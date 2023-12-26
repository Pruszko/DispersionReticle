package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.config.marker.DisposableExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.extended.CircleStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.DashedStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.PentagonStatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.StatefulRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.TShapeStatefulRenderer;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class ExtendedStatefulMarker extends StatefulMarker
	{
		
		private var _config:DisposableExtendedMarkerConfig;
		
		private var _shape:DisposableCustomShape;
		private var _outlineShape:DisposableCustomShape;
		private var _statefulRenderers:Object;
		
		public function ExtendedStatefulMarker(app:DispersionReticleFlash, gunMarkerType:int, extendedMarkerConfig:DisposableExtendedMarkerConfig)
		{
			super(app, gunMarkerType);
			
			this._config = extendedMarkerConfig;
			
			this._shape = new DisposableCustomShape()
			this.addChild(_shape);
			
			this._outlineShape = new DisposableCustomShape();
			this.addChild(_outlineShape);
			
			this._statefulRenderers = {
				"pentagon": new PentagonStatefulRenderer(this),
				"t-shape": new TShapeStatefulRenderer(this),
				"circle": new CircleStatefulRenderer(this),
				"dashed": new DashedStatefulRenderer(this)
			};
		}
		
		override public function disposeState() : void
		{
			this._shape.disposeState();
			this.removeChild(this._shape);
			this._shape = null;
			
			this._outlineShape.disposeState();
			this.removeChild(this._outlineShape);
			this._outlineShape = null;
			
			for (var propName:String in this._statefulRenderers)
			{
				this._statefulRenderers[propName].disposeState();
				delete _statefulRenderers[propName];
			}
			
			this._statefulRenderers = null;
			
			super.disposeState();
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			this.currentRenderer.updateState();
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			this.alpha = this._config.alpha;
			
			this._shape.setBlendStrength(this._config.blend);
			this._shape.clear();
			
			this._outlineShape.clear();
			
			this.currentRenderer.renderState();
		}
		
		private function get currentRenderer() : StatefulRenderer
		{
			if (this._statefulRenderers.hasOwnProperty(this._config.shape))
			{
				return this._statefulRenderers[this._config.shape];
			}
			
			this.app.warn("An unknown renderer for extended marker was attempted to be selected: " + this._config.shape);
			return this._statefulRenderers["pentagon"];
		}
		
		public function get shape() : DisposableCustomShape
		{
			return this._shape;
		}
		
		public function get outlineShape() : DisposableCustomShape
		{
			return this._outlineShape;
		}
		
		public function get config() : DisposableExtendedMarkerConfig
		{
			return this._config;
		}
		
	}

}