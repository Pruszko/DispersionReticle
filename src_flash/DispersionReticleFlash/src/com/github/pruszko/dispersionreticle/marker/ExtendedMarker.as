package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.config.marker.ExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.extended.CircleMarkerRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.DashedMarkerRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.PentagonMarkerRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.MarkerRenderer;
	import com.github.pruszko.dispersionreticle.marker.extended.TShapeMarkerRenderer;
	import com.github.pruszko.dispersionreticle.utils.CustomShape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class ExtendedMarker extends Marker
	{
		
		private var _config:ExtendedMarkerConfig;
		
		private var _shape:CustomShape;
		private var _outlineShape:CustomShape;
		private var _statefulRenderers:Object;
		
		public function ExtendedMarker(app:DispersionReticleFlash, reticleId:int, extendedMarkerConfig:ExtendedMarkerConfig)
		{
			super(app, reticleId);
			
			this._config = extendedMarkerConfig;
			
			this._shape = new CustomShape()
			this.addChild(_shape);
			
			this._outlineShape = new CustomShape();
			this.addChild(_outlineShape);
			
			this._statefulRenderers = {
				"pentagon": new PentagonMarkerRenderer(this),
				"t-shape": new TShapeMarkerRenderer(this),
				"circle": new CircleMarkerRenderer(this),
				"dashed": new DashedMarkerRenderer(this)
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
		
		private function get currentRenderer() : MarkerRenderer
		{
			if (this._statefulRenderers.hasOwnProperty(this._config.shape))
			{
				return this._statefulRenderers[this._config.shape];
			}
			
			this.app.warn("An unknown renderer for extended marker was attempted to be selected: " + this._config.shape);
			return this._statefulRenderers["pentagon"];
		}
		
		public function get shape() : CustomShape
		{
			return this._shape;
		}
		
		public function get outlineShape() : CustomShape
		{
			return this._outlineShape;
		}
		
		public function get config() :ExtendedMarkerConfig
		{
			return this._config;
		}
		
	}

}