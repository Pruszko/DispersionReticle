package com.github.pruszko.dispersionreticle
{
	import com.github.pruszko.dispersionreticle.config.DisposableConfig;
	import com.github.pruszko.dispersionreticle.config.marker.DisposableExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.StatefulMarker;
	import com.github.pruszko.dispersionreticle.marker.ExtendedStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.GunMarkerTypes;
	import flash.display.Sprite;
	import flash.events.Event;
	
	public class DispersionReticleFlash extends Sprite 
	{
		
		private static const SWF_HALF_WIDTH:Number = 400;
		private static const SWF_HALF_HEIGHT:Number = 300;
		
		// Scale used for rendering screen-size-dependent shapes
		private static const UNIT_SIZE_SCALE:Number = 0.001;
		
		// Python-side methods required for in-between game state updates
		public var py_warn:Function;
		public var py_getScreenResolution:Function;
		public var py_getNormalizedMarkerPosition:Function;
		
		private var _appWidth:Number = 0.0;
		private var _appHeight:Number = 0.0;
		private var _unitSize:Number = 0.0;
		
		private var _config:DisposableConfig = new DisposableConfig();
						
		public function DispersionReticleFlash() 
		{
			super();
		}
		
		public function as_populate() : void
		{
			this.addEventListener(Event.ENTER_FRAME, this.onEnterFrame);
		}
		
		public function as_dispose() : void
		{
			this.removeEventListener(Event.ENTER_FRAME, this.onEnterFrame);
			
			for (var i:int = 0; i < numChildren; ++i) {
				var marker:StatefulMarker = getMarkerAt(i);
				marker.disposeState();
			}
			
			this.removeChildren();
			
			this._config.disposeState();
			this._config = null;
		}
		
		public function as_createMarker(gunMarkerType:int, markerName:String) : void
		{
			var foundMarker:StatefulMarker = getMarkerByName(markerName);
			if (foundMarker != null) {
				this.warn("Present marker " + markerName + " was attempted to be spawned more than once");
				return;
			}
			
			var newMarker:StatefulMarker = null;
			
			// Gun marker types are present in python-side ReticleRegistry
			if (GunMarkerTypes.isExtendedReticle(gunMarkerType))
			{
				var extendedMarkerConfig:DisposableExtendedMarkerConfig = this._config.getExtendedMarkerConfig(gunMarkerType);
				
				if (extendedMarkerConfig == null)
				{
					warn("Could not find extended marker config for marker " + markerName + ".");
					return;
				}
				
				newMarker = new ExtendedStatefulMarker(this, gunMarkerType, extendedMarkerConfig);
			}
			else
			{
				warn("Unknown gun marker type received in as_createMarker: " +  + gunMarkerType);
				return;
			}
			
			newMarker.name = markerName;
			
			this.addChild(newMarker);
		}
		
		public function as_updateReticle(gunMarkerType:int, reticleSize:Number) : void
		{
			var markers:Vector.<StatefulMarker> = this.getMarkersByGunMarkerType(gunMarkerType);
			
			for (var i:int = 0; i < markers.length; ++i)
			{
				var marker:StatefulMarker = markers[i];
				
				if (marker.gunMarkerType != gunMarkerType)
				{
					continue;
				}
				
				marker.resetPartial();
				marker.reticleRadius = reticleSize / 2.0;
			}
			
			markers.splice(0, markers.length);
		}
		
		public function as_destroyMarker(markerName:String) : void
		{
			var foundMarker:StatefulMarker = this.getMarkerByName(markerName);
			if (foundMarker == null)
			{
				warn("Absent marker " + markerName + " were attempted to be removed");
				return;
			}
			
			this.removeChild(foundMarker);
			
			foundMarker.disposeState();
		}
		
		public function as_setMarkerDataProviderPresence(markerName:String, dataProviderPresence:Boolean) : void
		{
			var foundMarker:StatefulMarker = getMarkerByName(markerName);
			if (foundMarker == null)
			{
				// clearDataProvider() on our proxy can also be called when marker
				// is already destroyed
				// 
				// Just ignore such attempt and move on
				return;
			}
			
			foundMarker.hasDataProvider = dataProviderPresence;
		}
		
		public function as_onConfigReload(serializedConfig:Object) : void
		{
			this._config.deserialize(serializedConfig);
		}
		
		private function onEnterFrame() : void
		{
			this.updateAppPositionAndState();
			
			this.updateMarkersPositionAndVisibility();
			this.updateMarkers();
			this.renderMarkers();
		}
		
		private function updateAppPositionAndState() : void
		{
			if (this.py_getScreenResolution == null)
			{
				return;
			}
			
			// Update flash app position to exactly top-left corner
			// also update screen resolution dependent variables
			var screenResolution:Array = this.py_getScreenResolution();
			this._appWidth = screenResolution[0];
			this._appHeight = screenResolution[1];
			
			// This is based on updatePosition() from battleDamageIndicatorApp.swf
			// because it is the only source of "something is working" stuff 
			// and "visible in code" stuff when it comes to GUI.Flash
			//
			// Basically, our flash app center is positioned in the middle of the screen
			// with width and height declared in swf file
			// and despite having settings to change this behavior (position, size, anchors, etc)
			// from python-side on GUI.Flash, those does not work at all, lmao
			// 
			// To fix it ourselves, we have to:
			// - add half size of swf to anchor it to its left top corner in the middle of the screen
			// - substract half of the screen to move it to left top corner of the screen
			// 
			// Those changes MUST be done on flash object itself, not on GUI.Flash component
			this.x = SWF_HALF_WIDTH - (this.appWidth / 2.0);
			this.y = SWF_HALF_HEIGHT - (this.appHeight / 2.0);
			
			this._unitSize = 0.001 * this.appHeight;
			if (this.appWidth < this.appHeight)
			{
				this._unitSize = 0.001 * this.appWidth;
			}
		}
		
		private function updateMarkersPositionAndVisibility() : void
		{
			if (this.py_getNormalizedMarkerPosition == null)
			{
				return;
			}
			
			// Update all markers to proper 2d position starting from left-corner
			// also update their visibility in screen
			for (var i:int = 0; i < this.numChildren; ++i)
			{
				var marker:StatefulMarker = this.getMarkerAt(i);
				
				// General contract between this app and its python-side bridge is that
				// marker position access should occur only when marker has attached data provider
				if (!marker.hasDataProvider)
				{
					// Also, general contract between data providers and its display object is that
					// object is rendered only when data provider is attached
					marker.visible = false;
					continue;
				}
				
				var normalizedPosWithProjectionResult:Array = this.py_getNormalizedMarkerPosition(marker.name);
				var isPointOnScreen:Boolean = normalizedPosWithProjectionResult[2]
				
				marker.x = normalizedPosWithProjectionResult[0] * this.appWidth;
				marker.y = normalizedPosWithProjectionResult[1] * this.appHeight;
				marker.visible = isPointOnScreen;
			}
		}
		
		private function updateMarkers() : void
		{
			var i:Number;
			var marker:StatefulMarker;
			
			// used for in-between reticle updates variables interpolation
			for (i = 0; i < this.numChildren; ++i)
			{
				marker = this.getMarkerAt(i);
				marker.tickPartial();
			}
			
			for (i = 0; i < numChildren; ++i)
			{
				marker = this.getMarkerAt(i);
				
				if (!marker.hasDataProvider)
				{
					continue;
				}
				
				marker.updateState();
			}
		}
		
		private function renderMarkers() : void
		{
			for (var i:int = 0; i < this.numChildren; ++i)
			{
				var marker:StatefulMarker = getMarkerAt(i);
				
				if (!marker.hasDataProvider)
				{
					continue;
				}
				
				marker.renderState();
			}
		}
		
		public function getMarkerAt(index:int) : StatefulMarker
		{
			return this.getChildAt(index) as StatefulMarker;
		}
		
		public function getMarkerByName(markerName:String) : StatefulMarker
		{
			return this.getChildByName(markerName) as StatefulMarker;
		}
		
		public function getMarkersByGunMarkerType(gunMarkerType:int) : Vector.<StatefulMarker>
		{
			var markers:Vector.<StatefulMarker> = new Vector.<StatefulMarker>();
			for (var i:int = 0; i < this.numChildren; ++i)
			{
				var marker:StatefulMarker = this.getMarkerAt(i);
				
				if (marker.gunMarkerType == gunMarkerType)
				{
					markers.push(marker);
				}
			}
			
			return markers;
		}
		
		public function warn(message:String) : void
		{
			if (this.py_warn != null)
			{
				this.py_warn(message);
			}
		}
		
		public function get appWidth() : Number
		{
			return this._appWidth;
		}
		
		public function get appHeight() : Number
		{
			return this._appHeight;
		}
		
		public function get unitSize() : Number
		{
			return this._unitSize;
		}
		
		public function scaled(value:Number) : Number
		{
			var scaledValue:Number = value * this._unitSize;
			return scaledValue > 1.0 ? scaledValue : 1.0;
		}
		
		public function get config() : DisposableConfig
		{
			return this._config;
		}
		
	}
	
}