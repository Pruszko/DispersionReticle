package com.github.pruszko.dispersionreticle.config.marker.extended.shapes 
{
	
	public class DisposableExtendedMarkerShapesPentagonConfig 
	{
		
		private var _width:Number = 1.0;
		private var _height:Number = 1.0;
		
		public function DisposableExtendedMarkerShapesPentagonConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._width = serializedSection["width"];
			this._height = serializedSection["height"];
		}
		
		public function get width() : Number
		{
			return this._width;
		}
		
		public function get height() : Number
		{
			return this._height;
		}
		
	}

}