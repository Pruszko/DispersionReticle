package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.utils.Partial;
	import com.github.pruszko.dispersionreticle.utils.PartialValue;
	import com.github.pruszko.dispersionreticle.utils.Stateful;
	import flash.display.Sprite;
	
	public class Marker extends Sprite implements Stateful
	{
		
		private var _app:DispersionReticleFlash;
		private var _reticleId:int;
		
		private var _hasDataProvider:Boolean = false;
		
		// Reticle position is being accessed from python-side
		// because it is needed to be read from data providers
		// 
		// However, other reticle variables are being updated in controllers every 100 ms
		// so we have to interpolate them to render smoothly
		// between controller updates
		private var _partial:Partial = new Partial(100.0);
		private var _reticleRadius:PartialValue = new PartialValue(_partial, 0.0);
		
		public function Marker(app:DispersionReticleFlash, reticleId:int) 
		{
			super();
			this._app = app;
			this._reticleId = reticleId;
		}
		
		public function disposeState() : void
		{
			this._reticleRadius = null;
			
			this._partial.disposeState();
			this._partial = null;
			
			this._app = null;
		}
		
		public function updateState() : void
		{
			
		}
		
		public function renderState() : void
		{
			
		}
		
		public function resetPartial() : void
		{
			this._partial.reset();
		}
		
		public function tickPartial() : void
		{
			this._partial.tick();
		}
		
		public function get app() : DispersionReticleFlash
		{
			return this._app;
		}
		
		public function get reticleId() : int
		{
			return this._reticleId;
		}
		
		public function get reticleRadius() : Number
		{
			return this._reticleRadius.partial;
		}
		
		public function set reticleRadius(reticleRadius:Number) : void
		{
			this._reticleRadius.value = reticleRadius;
		}
		
		public function get hasDataProvider() : Boolean
		{
			return this._hasDataProvider;
		}
		
		public function set hasDataProvider(dataProviderPresence:Boolean) : void
		{
			this._hasDataProvider = dataProviderPresence;
		}
		
	}

}