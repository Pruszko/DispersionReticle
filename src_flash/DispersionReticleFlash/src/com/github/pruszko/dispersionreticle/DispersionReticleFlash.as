package com.github.pruszko.dispersionreticle
{
	import com.github.pruszko.dispersionreticle.marker.PentagonMarker;
	import com.github.pruszko.dispersionreticle.utils.Partial;
	import com.github.pruszko.dispersionreticle.utils.PartialValue;
	import flash.display.DisplayObject;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.external.ExternalInterface;
	import flash.geom.Point;
	import flash.utils.getTimer;
	
	public class DispersionReticleFlash extends Sprite 
	{
		
		private static const SWF_HALF_WIDTH:Number = 400;
		private static const SWF_HALF_HEIGHT:Number = 300;
		
		// For some reason reticle is slightly bigger than it should be
		// and it isn't caused by anything (scale, screen resolution etc)
		//
		// Just scaling it by this factor is precise enough, lmao
		private static const RETICLE_SIZE_FIX_MULTIPLIER:Number = 0.85;
		
		// Python-side methods required for in-between game state updates
		public var py_warn:Function;
		public var py_getScreenResolution:Function;
		public var py_getNormalizedMarkerPosition:Function;
		
		private var _appWidth:Number = 0.0;
		private var _appHeight:Number = 0.0;
		private var _fillColor:int = 0x0000FF;
		
		// Reticle position is being accessed from python-side
		// because it is needed to be read from data providers
		// 
		// However, reticle size is being updated in controllers every 100 ms
		// so we have to interpolate reticle size to render smoothly
		// between controller updates
		private var partial:Partial = new Partial(100.0);
		private var reticleSize:PartialValue = new PartialValue(partial, 32.0);
						
		public function DispersionReticleFlash() 
		{
			super();
		}
		
		public function as_populate() : void
		{
			addEventListener(Event.ENTER_FRAME, this.onEnterFrame);
		}
		
		public function as_dispose() : void
		{
			removeEventListener(Event.ENTER_FRAME, this.onEnterFrame);
			
			removeChildren();
			
			partial = null;
			reticleSize = null;
		}
		
		public function as_createMarker(markerName:String) : void
		{
			var foundMarker:DisplayObject = getChildByName(markerName);
			if (foundMarker != null) {
				warn("Present marker " + markerName + " were attempted to be spawned more than once");
				return;
			}
			
			var pentagonMarker:PentagonMarker = new PentagonMarker(this);
			pentagonMarker.name = markerName;
			pentagonMarker.visible = false
			
			addChild(pentagonMarker);
		}
		
		public function as_destroyMarker(markerName:String) : void
		{
			var foundMarker:DisplayObject = getChildByName(markerName);
			if (foundMarker == null) {
				warn("Absent marker " + markerName + " were attempted to be removed");
				return;
			}
			
			removeChild(foundMarker);
		}
		
		public function as_setMarkerVisibility(markerName:String, visible:Boolean) : void
		{
			var foundMarker:DisplayObject = getChildByName(markerName);
			if (foundMarker == null) {
				// clearDataProvider() on our proxy can also be called when marker
				// is already destroyed
				// 
				// Just ignore such attempt and move on
				return;
			}
			
			foundMarker.visible = visible;
		}
		
		// Called every controller updates to reset interpolation starting value
		public function as_tick() : void
		{
			partial.reset();
		}
		
		public function as_setReticleSize(reticleSize:Number) : void
		{
			this.reticleSize.value = reticleSize * RETICLE_SIZE_FIX_MULTIPLIER;
		}
		
		public function as_setFillColor(fillColor:int) : void
		{
			this._fillColor = fillColor;
		}
		
		public function as_setAlpha(alpha:Number) : void
		{
			this.alpha = alpha;
		}
		
		private function onEnterFrame() : void
		{
			// Update flash app position to exactly top-left corner
			if (this.py_getScreenResolution != null)
			{
				var screenResolution:Array = this.py_getScreenResolution();
				this._appWidth = screenResolution[0];
				this._appHeight = screenResolution[1];
				updatePosition();
			}
			
			// Update all markers to proper 2d position starting from left-corner
			if (this.py_getNormalizedMarkerPosition != null)
			{
				forEachPentagonMarker(updateMarkerPosition);
			}
			
			// Update partial for further interpolation
			partial.tick();
			
			// Rerender all pentagon markers
			forEachPentagonMarker(drawMarker);
		}
		
		private function forEachPentagonMarker(consumer:Function) : void
		{
			for (var i:int = 0; i < numChildren; ++i) {
				consumer(PentagonMarker(getChildAt(i)));
			}
		}
		
		private function updateMarkerPosition(pentagonMarker:PentagonMarker) : void
		{
			// General contract between this app and its python-side bridge is that
			// marker position access should occur only when marker is visible
			if (!pentagonMarker.visible) {
				return;
			}
			
			var normalizedPosWithProjectionResult:Array = this.py_getNormalizedMarkerPosition(pentagonMarker.name);
			var isPointOnScreen:Boolean = normalizedPosWithProjectionResult[2]
			
			pentagonMarker.x = normalizedPosWithProjectionResult[0] * this.appWidth;
			pentagonMarker.y = normalizedPosWithProjectionResult[1] * this.appHeight;
			pentagonMarker.isOnScreen = isPointOnScreen;
		}
		
		private function drawMarker(pentagonMarker:PentagonMarker) : void
		{
			pentagonMarker.draw(this.reticleSize.partial);
		}
		
		private function updatePosition() : void
		{
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
		
		public function get appWidth() : Number
		{
			return _appWidth;
		}
		
		public function get appHeight() : Number
		{
			return _appHeight;
		}
		
		public function get fillColor() : int
		{
			return _fillColor;
		}
		
		private function warn(message:String) : void
		{
			if (py_warn != null) {
				py_warn(message);
			}
		}
		
	}
	
}