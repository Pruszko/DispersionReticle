package com.github.pruszko.dispersionreticle.utils 
{
	import flash.display.Shape;
	
	public class ShapeFragment implements Disposable
	{
		
		private var _shape:Shape;
		
		private var _anchorX:Number = 0.0;
		private var _anchorY:Number = 0.0;
		
		private var _angleSin:Number = 0.0;
		private var _angleCos:Number = 1.0;
		
		public function ShapeFragment(shape:Shape) 
		{
			super();
			this._shape = shape;
			this._anchorX = 0.0;
			this._anchorY = 0.0;
		}
		
		public function disposeState() : void
		{
			this._shape = null;
		}
		
		public function setAnchor(anchorX:Number, anchorY:Number) : void
		{
			this._anchorX = anchorX;
			this._anchorY = anchorY;
		}
		
		public function setAngleDeg(angleDeg:Number) : void
		{
			this.setAngleRad(Math.PI * angleDeg / 180.0);
		}
		
		public function setAngleRad(angleRad:Number) : void
		{
			this._angleSin = Math.sin(-angleRad);
			this._angleCos = Math.cos(-angleRad);
		}
		
		public function moveTo(x:Number, y:Number) : void
		{
			x -= this._anchorX;
			y -= this._anchorY;
			
			var newX:Number = x * this._angleCos - y * this._angleSin;
			var newY:Number = x * this._angleSin + y * this._angleCos;
			
			x = this._anchorX + newX;
			y = this._anchorY + newY;
			
			this._shape.graphics.moveTo(x, y);
		}
		
		public function lineTo(x:Number, y:Number) : void
		{
			x -= this._anchorX;
			y -= this._anchorY;
			
			var newX:Number = x * this._angleCos - y * this._angleSin;
			var newY:Number = x * this._angleSin + y * this._angleCos;
			
			x = this._anchorX + newX;
			y = this._anchorY + newY;
			
			this._shape.graphics.lineTo(x, y);
		}
		
		public function drawCircle(x:Number, y:Number, radius:Number) : void
		{
			x -= this._anchorX;
			y -= this._anchorY;
			
			var newX:Number = x * this._angleCos - y * this._angleSin;
			var newY:Number = x * this._angleSin + y * this._angleCos;
			
			x = this._anchorX + newX;
			y = this._anchorY + newY;
			
			this._shape.graphics.drawCircle(x, y, radius);
		}
		
	}

}