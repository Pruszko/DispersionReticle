package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.marker.SimpleStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import com.github.pruszko.dispersionreticle.utils.Stateful;
	
	
	public class StatefulRenderer implements Stateful
	{
		
		private var _simpleMarker:SimpleStatefulMarker;
		
		public function StatefulRenderer(simpleMarker:SimpleStatefulMarker) 
		{
			this._simpleMarker = simpleMarker;
		}
		
		public function disposeState() : void
		{
			this._simpleMarker = null;
		}
		
		public function updateState() : void
		{
			
		}
		
		public function renderState() : void
		{
			
		}
		
		protected function get simpleMarker() : SimpleStatefulMarker
		{
			return _simpleMarker;
		}
		
		protected function get app() : DispersionReticleFlash
		{
			return simpleMarker.app;
		}
		
		protected function get shape() : DisposableCustomShape
		{
			return simpleMarker.shape;
		}
		
		protected function get outlineShape() : DisposableCustomShape
		{
			return simpleMarker.outlineShape;
		}
		
		protected function scaleLogByReticleRadius(value:Number) : Number
		{
			return app.scaled(value * (100.0 + reticleRadius) / 100.0);
		}
		
		protected function get reticleRadius() : Number
		{
			return simpleMarker.reticleRadius;
		}
		
		protected function get fillColor() : Number
		{
			return simpleMarker.fillColor;
		}
		
		public function get selectedShape() : String
		{
			return simpleMarker.selectedShape;
		}
		
		public function get shouldDrawCenterDot() : Boolean
		{
			return simpleMarker.shouldDrawCenterDot;
		}
		
		public function get shouldDrawOutline() : Boolean
		{
			return simpleMarker.shouldDrawOutline;
		}
		
	}
	
}