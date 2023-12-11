package com.github.pruszko.dispersionreticle.config.marker 
{
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class DisposableCustomMarkerConfig implements Disposable
	{
		
		private var _shape:String = "pentagon";
		private var _color:int = 0xFF00FF;
		private var _drawCenterDot:Boolean = false;
		private var _drawOutline:Boolean = false;
		private var _blend:Number = 0.8;
		private var _alpha:Number = 1.0;
		
		public function DisposableCustomMarkerConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._shape = serializedSection["shape"];
			this._color = serializedSection["color"];
			this._drawCenterDot = serializedSection["draw-center-dot"];
			this._drawOutline = serializedSection["draw-outline"];
			this._blend = serializedSection["blend"];
			this._alpha = serializedSection["alpha"];
		}
		
		public function get shape() : String
		{
			return _shape;
		}
		
		public function get color() : int
		{
			return _color;
		}
		
		public function get drawCenterDot() : Boolean
		{
			return _drawCenterDot;
		}
		
		public function get drawOutline() : Boolean
		{
			return _drawOutline;
		}
		
		public function get blend() : Number
		{
			return _blend;
		}
		
		public function get alpha() : Number
		{
			return _alpha;
		}
		
	}

}