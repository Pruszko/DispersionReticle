package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.config.marker.DisposableCustomMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.simple.CircleStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.DashedStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.PentagonStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.StatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.simple.TShapeStatefulRenderer;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class CustomStatefulMarker extends StatefulMarker
	{
		
		private var _customMarkerConfig:DisposableCustomMarkerConfig;
		
		private var _shape:DisposableCustomShape;
		private var _outlineShape:DisposableCustomShape;
		private var _statefulRenderers:Object;
		
		public function CustomStatefulMarker(app:DispersionReticleFlash, gunMarkerType:int, customMarkerConfig:DisposableCustomMarkerConfig)
		{
			super(app, gunMarkerType);
			
			this._customMarkerConfig = customMarkerConfig;
			
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
			
			this.alpha = _customMarkerConfig.alpha;
			
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
			return _customMarkerConfig.color;
		}
		
		public function get selectedShape() : String
		{
			return _customMarkerConfig.shape;
		}
		
		public function get blendStrength() : Number
		{
			return _customMarkerConfig.blend;
		}
		
		public function get shouldDrawCenterDot() : Boolean
		{
			return _customMarkerConfig.drawCenterDot;
		}
		
		public function get shouldDrawOutline() : Boolean
		{
			return _customMarkerConfig.drawOutline;
		}
		
	}

}