package com.github.pruszko.dispersionreticle.config.marker.extended.shapes 
{
	
	public class DisposableExtendedMarkerShapesTShapeConfig 
	{
		
		private var _thickness:Number = 1.0;
		private var _length:Number = 1.0;
		
		public function DisposableExtendedMarkerShapesTShapeConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._thickness = serializedSection["thickness"];
			this._length = serializedSection["length"];
		}
		
		public function get thickness() : Number
		{
			return this._thickness;
		}
		
		public function get length() : Number
		{
			return this._length;
		}
		
	}

}