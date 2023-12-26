package com.github.pruszko.dispersionreticle.marker.extended 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.config.marker.DisposableExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.marker.ExtendedStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.DisposableCustomShape;
	import com.github.pruszko.dispersionreticle.utils.Stateful;
	import com.github.pruszko.dispersionreticle.utils.Utils;
	
	
	public class StatefulRenderer implements Stateful
	{
		
		private var _extendedMarker:ExtendedStatefulMarker;
		
		public function StatefulRenderer(extendedMarker:ExtendedStatefulMarker) 
		{
			this._extendedMarker = extendedMarker;
		}
		
		public function disposeState() : void
		{
			this._extendedMarker = null;
		}
		
		public function updateState() : void
		{
			
		}
		
		public function renderState() : void
		{
			
		}
		
		protected function get extendedMarker() : ExtendedStatefulMarker
		{
			return this._extendedMarker;
		}
		
		protected function get app() : DispersionReticleFlash
		{
			return this.extendedMarker.app;
		}
		
		protected function get shape() : DisposableCustomShape
		{
			return this.extendedMarker.shape;
		}
		
		protected function get outlineShape() : DisposableCustomShape
		{
			return this.extendedMarker.outlineShape;
		}
		
		// I've spend way too much time to improve
		// this scalling for figure-based shapes
		// and exactly this function works perfectly.
		//
		// At first there was something resembling "logarithmic fuction" (no, it wasn't):
		// Y = value * (100.0 + reticleSize) / 100.0
		// however, when reticleSize was small, shape was too big
		// covering most part of default reticles due to quite large initial size.
		//
		// Then I tried to use actual logarithmic scalling, something like:
		// Y = value * log[b](1 + a * reticleSize)
		// with various log base "b" and reticle size multipliers "a"
		// however, no matter what I've chosen, "something was off"
		// with how reticle scalling felt.
		// 
		// I even made excel spreadsheet to "see" values in scale I'd tried to match.
		//
		// Then I just used basic square root with simple 0.9 multiplier 
		// and it feels perfectly natural right away, lmao.
		protected function scaleSqrtByReticleRadius(value:Number) : Number
		{
			return value * 0.9 * Math.sqrt(this.reticleRadius);
		}
		
		protected function get reticleRadius() : Number
		{
			return this.extendedMarker.reticleRadius;
		}
		
		protected function get config() : DisposableExtendedMarkerConfig
		{
			return this.extendedMarker.config;
		}
		
	}
	
}