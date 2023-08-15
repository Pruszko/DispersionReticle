package com.github.pruszko.dispersionreticle.config 
{
	import com.github.pruszko.dispersionreticle.config.marker.DisposableSimpleMarkerConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class DisposableConfig implements Disposable
	{
		
		private var _simpleServerReticle:DisposableSimpleMarkerConfig = new DisposableSimpleMarkerConfig();
		
		public function DisposableConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			_simpleServerReticle.disposeState();
			_simpleServerReticle = null;
		}
		
		public function deserialize(serializedConfig:Object) : void
		{
			this.simpleServerReticle.deserialize(serializedConfig["simple-server-reticle"]);
		}
		
		public function get simpleServerReticle() : DisposableSimpleMarkerConfig
		{
			return _simpleServerReticle;
		}
		
	}

}