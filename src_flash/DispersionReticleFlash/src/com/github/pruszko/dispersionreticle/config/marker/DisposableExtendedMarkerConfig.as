package com.github.pruszko.dispersionreticle.config.marker 
{
	import com.github.pruszko.dispersionreticle.config.marker.extended.DisposableExtendedMarkerShapesConfig;
	import com.github.pruszko.dispersionreticle.utils.Disposable;
	
	public class DisposableExtendedMarkerConfig implements Disposable
	{
		
		private var _shape:String = "pentagon";
		private var _color:int = 0xFF00FF;
		private var _drawCenterDot:Boolean = false;
		private var _drawOutline:Boolean = false;
		private var _blend:Number = 0.8;
		private var _alpha:Number = 1.0;
		private var _shapes:DisposableExtendedMarkerShapesConfig = new DisposableExtendedMarkerShapesConfig();
		
		public function DisposableExtendedMarkerConfig() 
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
			this._drawCenterDot = serializedSection["draw-center-dot"];
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
		
		public function get drawCenterDot() : Boolean
		{
			return this._drawCenterDot;
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
		
		public function get shapes() : DisposableExtendedMarkerShapesConfig
		{
			return this._shapes;
		}
		
	}

}