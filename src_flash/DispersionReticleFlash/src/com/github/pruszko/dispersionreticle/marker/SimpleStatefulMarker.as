package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.marker.simple.CircleStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.DashedStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.PentagonStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.StatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.TShapeStatefulRenderer;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class SimpleStatefulMarker extends StatefulMarker
	{
		
		public static const GUN_MARKER_TYPE:int = 7;
		
		private var _shape:DisposableCustomShape;
		private var _outlineShape:DisposableCustomShape;
		private var _statefulRenderers:Object;
		
		public function SimpleStatefulMarker(app:DispersionReticleFlash, gunMarkerType:int, isServerReticle:Boolean)
		{
			super(app, gunMarkerType, isServerReticle);
			
			this._shape = new DisposableCustomShape()
			addChild(_shape);
			
			this._outlineShape = new DisposableCustomShape();
			addChild(_outlineShape);
			
			_statefulRenderers = {
				"pentagon": new PentagonStatefulRenderer(this),
				"t-shape": new TShapeStatefulRenderer(this),
				"circle": new CircleStatefulRenderer(this),
				"dashed": new DashedStatefulRenderer(this)
			};
		}
		
		override public function disposeState() : void
		{
			_shape.disposeState();
			removeChild(_shape);
			this._shape = null;
			
			_outlineShape.disposeState();
			removeChild(_outlineShape);
			this._outlineShape = null;
			
			for (var propName:String in _statefulRenderers)
			{
				_statefulRenderers[propName].disposeState();
				delete _statefulRenderers[propName];
			}
			
			_statefulRenderers = null;
			
			super.disposeState();
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			currentRenderer.updateState();
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			this.alpha = app.config.simpleServerReticle.alpha
			
			_shape.setBlendStrength(blendStrength);
			_shape.clear();
			
			_outlineShape.clear();
			
			currentRenderer.renderState();
		}
		
		private function get currentRenderer() : StatefulRenderer
		{
			if (_statefulRenderers.hasOwnProperty(selectedShape))
			{
				return _statefulRenderers[selectedShape];
			}
			
			app.warn("An unknown renderer for simple marker was attempted to be selected: " + selectedShape);
			return _statefulRenderers["pentagon"];
		}
		
		public function get shape() : DisposableCustomShape
		{
			return _shape;
		}
		
		public function get outlineShape() : DisposableCustomShape
		{
			return _outlineShape;
		}
		
		public function get fillColor() : Number
		{
			return app.config.simpleServerReticle.color;
		}
		
		public function get selectedShape() : String
		{
			return app.config.simpleServerReticle.shape;
		}
		
		public function get blendStrength() : Number
		{
			return app.config.simpleServerReticle.blend;
		}
		
		public function get shouldDrawCenterDot() : Boolean
		{
			return app.config.simpleServerReticle.drawCenterDot;
		}
		
		public function get shouldDrawOutline() : Boolean
		{
			return app.config.simpleServerReticle.drawOutline;
		}
		
	}

}