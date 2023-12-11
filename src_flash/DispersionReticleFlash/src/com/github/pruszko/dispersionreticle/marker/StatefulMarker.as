package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import com.github.pruszko.dispersionreticle.utils.DisposablePartial;
	import com.github.pruszko.dispersionreticle.utils.DisposablePartialValue;
	import com.github.pruszko.dispersionreticle.utils.Stateful;
	import flash.display.Sprite;
	
	public class StatefulMarker extends Sprite implements Stateful
	{
		
		private var _app:DispersionReticleFlash;
		private var _gunMarkerType:int;
		
		private var _hasDataProvider:Boolean = false;
		
		// Reticle position is being accessed from python-side
		// because it is needed to be read from data providers
		// 
		// However, other reticle variables are being updated in controllers every 100 ms
		// so we have to interpolate them to render smoothly
		// between controller updates
		private var _partial:DisposablePartial = new DisposablePartial(100.0);
		private var _reticleRadius:DisposablePartialValue = new DisposablePartialValue(_partial, 0.0);
		
		public function StatefulMarker(app:DispersionReticleFlash, gunMarkerType:int) 
		{
			super();
			this._app = app;
			this._gunMarkerType = gunMarkerType;
		}
		
		public function disposeState() : void
		{
			_reticleRadius = null;
			
			_partial.disposeState();
			_partial = null;
			
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
			return _app;
		}
		
		public function get gunMarkerType() : int
		{
			return _gunMarkerType;
		}
		
		public function get reticleRadius() : Number
		{
			return _reticleRadius.partial;
		}
		
		public function set reticleRadius(reticleRadius:Number) : void
		{
			this._reticleRadius.value = reticleRadius;
		}
		
		public function get hasDataProvider() : Boolean
		{
			return _hasDataProvider;
		}
		
		public function set hasDataProvider(dataProviderPresence:Boolean) : void
		{
			this._hasDataProvider = dataProviderPresence;
		}
		
	}

}