package com.github.pruszko.dispersionreticle.config 
{
	import com.github.pruszko.dispersionreticle.config.marker.DisposableExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	import com.github.pruszko.dispersionreticle.utils.GunMarkerTypes;
	
	public class DisposableConfig implements Disposable
	{
		
		private var _focusedReticleExtended:DisposableExtendedMarkerConfig = new DisposableExtendedMarkerConfig();
		private var _hybridReticleExtended:DisposableExtendedMarkerConfig = new DisposableExtendedMarkerConfig();
		private var _serverReticleExtended:DisposableExtendedMarkerConfig = new DisposableExtendedMarkerConfig();
		
		public function DisposableConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			_focusedReticleExtended.disposeState();
			_focusedReticleExtended = null;
			_hybridReticleExtended.disposeState();
			_hybridReticleExtended = null;
			_serverReticleExtended.disposeState();
			_serverReticleExtended = null;
		}
		
		public function deserialize(serializedConfig:Object) : void
		{
			this._focusedReticleExtended.deserialize(serializedConfig["focused-reticle-extended"]);
			this._hybridReticleExtended.deserialize(serializedConfig["hybrid-reticle-extended"]);
			this._serverReticleExtended.deserialize(serializedConfig["server-reticle-extended"]);
		}
		
		public function getExtendedMarkerConfig(gunMarkerType:int) : DisposableExtendedMarkerConfig
		{
			switch (gunMarkerType)
			{
				case GunMarkerTypes.FOCUSED_EXTENDED_CLIENT:
				case GunMarkerTypes.FOCUSED_EXTENDED_SERVER:
					return _focusedReticleExtended;
				case GunMarkerTypes.HYBRID_EXTENDED_CLIENT:
					return _hybridReticleExtended;
				case GunMarkerTypes.SERVER_EXTENDED_SERVER:
					return _serverReticleExtended;
				default:
					return null;
			}
		}
	
		
	}

}