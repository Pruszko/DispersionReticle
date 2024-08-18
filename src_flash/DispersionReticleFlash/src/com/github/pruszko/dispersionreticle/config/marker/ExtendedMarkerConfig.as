package com.github.pruszko.dispersionreticle.config.marker 
{
	import com.github.pruszko.dispersionreticle.config.marker.extended.ExtendedMarkerShapesConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class ExtendedMarkerConfig implements Disposable
	{
		
		private var _shape:String = "pentagon";
		private var _color:int = 0xFF00FF;
		private var _centerDotSize:Number = 0.0;
		private var _drawOutline:Boolean = false;
		private var _blend:Number = 0.8;
		private var _alpha:Number = 1.0;
		private var _shapes:ExtendedMarkerShapesConfig = new ExtendedMarkerShapesConfig();
		
		public function ExtendedMarkerConfig() 
		{
			super();
		}
		
		public function disposeState() : void
		{
			this._shapes.disposeState();
			this._shapes = null;
		}
		
		public function deserialize(serializedSection:Object) : void
		{
			this._shape = serializedSection["shape"];
			this._color = serializedSection["color"];
			this._centerDotSize = serializedSection["center-dot-size"];
			this._drawOutline = serializedSection["draw-outline"];
			this._blend = serializedSection["blend"];
			this._alpha = serializedSection["alpha"];
			this._shapes.deserialize(serializedSection["shapes"]);
		}
		
		public function get shape() : String
		{
			return this._shape;
		}
		
		public function get color() : int
		{
			return this._color;
		}
		
		public function get centerDotSize() : Number
		{
			return this._centerDotSize;
		}
		
		public function get drawOutline() : Boolean
		{
			return this._drawOutline;
		}
		
		public function get blend() : Number
		{
			return this._blend;
		}
		
		public function get alpha() : Number
		{
			return this._alpha;
		}
		
		public function get shapes() : ExtendedMarkerShapesConfig
		{
			return this._shapes;
		}
		
	}

}