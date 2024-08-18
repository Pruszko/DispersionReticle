package com.github.pruszko.dispersionreticle
{
	import com.github.pruszko.dispersionreticle.config.Config;
	import com.github.pruszko.dispersionreticle.config.marker.ExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.Marker;
	import com.github.pruszko.dispersionreticle.marker.ExtendedMarker;
	import com.github.pruszko.dispersionreticle.utils.ReticleTypes;
	import flash.display.Sprite;
	import flash.events.Event;
	
	public class DispersionReticleFlash extends Sprite 
	{
		
		private static const SWF_HALF_WIDTH:Number = 400;
		private static const SWF_HALF_HEIGHT:Number = 300;
		
		// Python-side methods required for in-between game state updates
		public var py_warn:Function;
		public var py_getScreenResolution:Function;
		public var py_getNormalizedMarkerPosition:Function;
		
		private var _appWidth:Number = 0.0;
		private var _appHeight:Number = 0.0;
		
		private var _config:Config = new Config();
						
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
			
			for (var i:int = 0; i < this.numChildren; ++i) {
				var marker:Marker = this.getMarkerAt(i);
				marker.disposeState();
			}
			
			this.removeChildren();
			
			this._config.disposeState();
			this._config = null;
		}
		
		public function as_createMarker(reticleId:int, markerName:String) : void
		{
			var foundMarker:Marker = this.getMarkerByName(markerName);
			if (foundMarker != null) {
				this.warn("Present marker " + markerName + " was attempted to be spawned more than once");
				return;
			}
			
			var newMarker:Marker = null;
			
			// Reticle types are present in python-side ReticleTypes
			if (ReticleTypes.isExtendedReticle(reticleId))
			{
				var extendedMarkerConfig:ExtendedMarkerConfig = this._config.getExtendedMarkerConfig(reticleId);
				if (extendedMarkerConfig == null)
				{
					this.warn("Could not find extended marker config for marker " + markerName + ".");
					return;
				}
				
				newMarker = new ExtendedMarker(this, reticleId, extendedMarkerConfig);
			}
			else
			{
				this.warn("Unknown reticle id received in as_createMarker: " +  + reticleId);
				return;
			}
			
			newMarker.name = markerName;
			
			this.addChild(newMarker);
		}
		
		public function as_updateReticle(reticleId:int, reticleSize:Number) : void
		{			
			for (var i:int = 0; i < this.numChildren; ++i)
			{
				var marker:Marker = this.getMarkerAt(i);
				
				if (marker.reticleId != reticleId)
				{
					continue;
				}
				
				marker.resetPartial();
				marker.reticleRadius = reticleSize / 2.0;
			}
		}
		
		public function as_destroyMarker(markerName:String) : void
		{
			var foundMarker:Marker = this.getMarkerByName(markerName);
			if (foundMarker == null)
			{
				this.warn("Absent marker " + markerName + " were attempted to be removed");
				return;
			}
			
			this.removeChild(foundMarker);
			
			foundMarker.disposeState();
		}
		
		public function as_setMarkerDataProviderPresence(markerName:String, dataProviderPresence:Boolean) : void
		{
			var foundMarker:Marker = this.getMarkerByName(markerName);
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
				var marker:Marker = this.getMarkerAt(i);
				
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
			var marker:Marker;
			
			// used for in-between reticle updates variables interpolation
			for (i = 0; i < this.numChildren; ++i)
			{
				marker = this.getMarkerAt(i);
				marker.tickPartial();
			}
			
			for (i = 0; i < this.numChildren; ++i)
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
				var marker:Marker = getMarkerAt(i);
				
				if (!marker.hasDataProvider)
				{
					continue;
				}
				
				marker.renderState();
			}
		}
		
		public function getMarkerAt(index:int) : Marker
		{
			return this.getChildAt(index) as Marker;
		}
		
		public function getMarkerByName(markerName:String) : Marker
		{
			return this.getChildByName(markerName) as Marker;
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
		
		public function get config() : Config
		{
			return this._config;
		}
		
	}
	
}