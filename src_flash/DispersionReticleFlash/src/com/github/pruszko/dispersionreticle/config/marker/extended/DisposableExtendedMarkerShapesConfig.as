package com.github.pruszko.dispersionreticle.config.marker.extended 
{
	import com.github.pruszko.dispersionreticle.config.marker.extended.shapes.DisposableExtendedMarkerShapesPentagonConfig;
	import com.github.pruszko.dispersionreticle.config.marker.extended.shapes.DisposableExtendedMarkerShapesTShapeConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class DisposableExtendedMarkerShapesConfig implements Disposable
	{
		
		private var _pentagon:DisposableExtendedMarkerShapesPentagonConfig = new DisposableExtendedMarkerShapesPentagonConfig();
		private var _tshape:DisposableExtendedMarkerShapesTShapeConfig = new DisposableExtendedMarkerShapesTShapeConfig();
		
		public function DisposableExtendedMarkerShapesConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			this._pentagon.disposeState();
			this._pentagon = null;
			this._tshape.disposeState();
			this._tshape = null;
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._pentagon.deserialize(serializedSection["pentagon"]);
			this._tshape.deserialize(serializedSection["t-shape"]);
		}
		
		public function get pentagon() : DisposableExtendedMarkerShapesPentagonConfig
		{
			return this._pentagon;
		}
		
		public function get tshape() : DisposableExtendedMarkerShapesTShapeConfig
		{
			return this._tshape;
		}
		
	}

}