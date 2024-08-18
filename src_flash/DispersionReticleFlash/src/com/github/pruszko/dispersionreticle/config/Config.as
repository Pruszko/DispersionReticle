package com.github.pruszko.dispersionreticle.config 
{
	import com.github.pruszko.dispersionreticle.config.marker.ExtendedMarkerConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	import com.github.pruszko.dispersionreticle.utils.ReticleTypes;
	
	public class Config implements Disposable
	{
		
		private var _focusedReticleExtended:ExtendedMarkerConfig = new ExtendedMarkerConfig();
		private var _hybridReticleExtended:ExtendedMarkerConfig = new ExtendedMarkerConfig();
		private var _serverReticleExtended:ExtendedMarkerConfig = new ExtendedMarkerConfig();
		
		public function Config() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			this._focusedReticleExtended.disposeState();
			this._focusedReticleExtended = null;
			this._hybridReticleExtended.disposeState();
			this._hybridReticleExtended = null;
			this._serverReticleExtended.disposeState();
			this._serverReticleExtended = null;
		}
		
		public function deserialize(serializedConfig:Object) : void
		{
			this._focusedReticleExtended.deserialize(serializedConfig["focused-reticle-extended"]);
			this._hybridReticleExtended.deserialize(serializedConfig["hybrid-reticle-extended"]);
			this._serverReticleExtended.deserialize(serializedConfig["server-reticle-extended"]);
		}
		
		public function getExtendedMarkerConfig(reticleId:int) : ExtendedMarkerConfig
		{
			switch (reticleId)
			{
				case ReticleTypes.FOCUSED_EXTENDED:
					return this._focusedReticleExtended;
				case ReticleTypes.HYBRID_EXTENDED:
					return this._hybridReticleExtended;
				case ReticleTypes.SERVER_EXTENDED:
					return this._serverReticleExtended;
				default:
					return null;
			}
		}
		
	}

}