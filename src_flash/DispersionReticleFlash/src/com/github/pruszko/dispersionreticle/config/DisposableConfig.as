package com.github.pruszko.dispersionreticle.config 
{
	import com.github.pruszko.dispersionreticle.config.marker.DisposableCustomMarkerConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	import com.github.pruszko.dispersionreticle.utils.GunMarkerTypes;
	
	public class DisposableConfig implements Disposable
	{
		
		private var _customFocusedReticle:DisposableCustomMarkerConfig = new DisposableCustomMarkerConfig();
		private var _customHybridReticle:DisposableCustomMarkerConfig = new DisposableCustomMarkerConfig();
		private var _customServerReticle:DisposableCustomMarkerConfig = new DisposableCustomMarkerConfig();
		
		public function DisposableConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			_customFocusedReticle.disposeState();
			_customFocusedReticle = null;
			_customHybridReticle.disposeState();
			_customHybridReticle = null;
			_customServerReticle.disposeState();
			_customServerReticle = null;
		}
		
		public function deserialize(serializedConfig:Object) : void
		{
			this._customFocusedReticle.deserialize(serializedConfig["custom-focused-reticle"]);
			this._customHybridReticle.deserialize(serializedConfig["custom-hybrid-reticle"]);
			this._customServerReticle.deserialize(serializedConfig["custom-server-reticle"]);
		}
		
		public function getCustomMarkerConfig(gunMarkerType:int) : DisposableCustomMarkerConfig
		{
			switch (gunMarkerType)
			{
				case GunMarkerTypes.CUSTOM_FOCUSED_CLIENT:
				case GunMarkerTypes.CUSTOM_FOCUSED_SERVER:
					return _customFocusedReticle;
				case GunMarkerTypes.CUSTOM_HYBRID_CLIENT:
					return _customHybridReticle;
				case GunMarkerTypes.CUSTOM_SERVER_SERVER:
					return _customServerReticle;
				default:
					return null;
			}
		}
		
		public function get customFocusedReticle() : DisposableCustomMarkerConfig
		{
			return _customFocusedReticle;
		}
		
		public function get customHybridReticle() : DisposableCustomMarkerConfig
		{
			return _customHybridReticle;
		}
		
		public function get customServerReticle() : DisposableCustomMarkerConfig
		{
			return _customServerReticle;
		}
		
	}

}