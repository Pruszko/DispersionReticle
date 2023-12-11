package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.marker.CustomStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import com.github.pruszko.dispersionreticle.utils.Stateful;
	
	
	public class StatefulRenderer implements Stateful
	{
		
		private var _customMarker:CustomStatefulMarker;
		
		public function StatefulRenderer(customMarker:CustomStatefulMarker) 
		{
			this._customMarker = customMarker;
		}
		
		public function disposeState() : void
		{
			this._customMarker = null;
		}
		
		public function updateState() : void
		{
			
		}
		
		public function renderState() : void
		{
			
		}
		
		protected function get customMarker() : CustomStatefulMarker
		{
			return _customMarker;
		}
		
		protected function get app() : DispersionReticleFlash
		{
			return customMarker.app;
		}
		
		protected function get shape() : DisposableCustomShape
		{
			return customMarker.shape;
		}
		
		protected function get outlineShape() : DisposableCustomShape
		{
			return customMarker.outlineShape;
		}
		
		protected function scaleLogByReticleRadius(value:Number) : Number
		{
			return app.scaled(value * (100.0 + reticleRadius) / 100.0);
		}
		
		protected function get reticleRadius() : Number
		{
			return customMarker.reticleRadius;
		}
		
		protected function get fillColor() : Number
		{
			return customMarker.fillColor;
		}
		
		public function get selectedShape() : String
		{
			return customMarker.selectedShape;
		}
		
		public function get shouldDrawCenterDot() : Boolean
		{
			return customMarker.shouldDrawCenterDot;
		}
		
		public function get shouldDrawOutline() : Boolean
		{
			return customMarker.shouldDrawOutline;
		}
		
	}
	
}