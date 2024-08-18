package com.github.pruszko.dispersionreticle.config.marker.extended 
{
	import com.github.pruszko.dispersionreticle.config.marker.extended.shapes.ExtendedMarkerShapesPentagonConfig;
	import com.github.pruszko.dispersionreticle.config.marker.extended.shapes.ExtendedMarkerShapesTShapeConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class ExtendedMarkerShapesConfig implements Disposable
	{
		
		private var _pentagon:ExtendedMarkerShapesPentagonConfig = new ExtendedMarkerShapesPentagonConfig();
		private var _tshape:ExtendedMarkerShapesTShapeConfig = new ExtendedMarkerShapesTShapeConfig();
		
		public function ExtendedMarkerShapesConfig() 
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
		
		public function get pentagon() : ExtendedMarkerShapesPentagonConfig
		{
			return this._pentagon;
		}
		
		public function get tshape() : ExtendedMarkerShapesTShapeConfig
		{
			return this._tshape;
		}
		
	}

}