package com.github.pruszko.dispersionreticle.utils 
{
	import flash.display.Shape;
	
	public class DisposableShapeFragment implements Disposable
	{
		
		private var _shape:Shape;
		
		private var _anchorX:Number = 0.0;
		private var _anchorY:Number = 0.0;
		
		private var _angleSin:Number = 0.0;
		private var _angleCos:Number = 1.0;
		
		public function DisposableShapeFragment(shape:Shape) 
		{
			super();
			this._shape = shape;
			this._anchorX = 0.0;
			this._anchorY = 0.0;
		}
		
		public function disposeState() : void
		{
			_shape = null;
		}
		
		public function setAnchor(anchorX:Number, anchorY:Number) : void
		{
			this._anchorX = anchorX;
			this._anchorY = anchorY;
		}
		
		public function setAngleDeg(angleDeg:Number) : void
		{
			setAngleRad(Math.PI * angleDeg / 180.0);
		}
		
		public function setAngleRad(angleRad:Number) : void
		{
			this._angleSin = Math.sin(-angleRad);
			this._angleCos = Math.cos(-angleRad);
		}
		
		public function moveTo(x:Number, y:Number) : void
		{
			x -= _anchorX;
			y -= _anchorY;
			
			var newX:Number = x * _angleCos - y * _angleSin;
			var newY:Number = x * _angleSin + y * _angleCos;
			
			x = _anchorX + newX;
			y = _anchorY + newY;
			
			_shape.graphics.moveTo(x, y);
		}
		
		public function lineTo(x:Number, y:Number) : void
		{
			x -= _anchorX;
			y -= _anchorY;
			
			var newX:Number = x * _angleCos - y * _angleSin;
			var newY:Number = x * _angleSin + y * _angleCos;
			
			x = _anchorX + newX;
			y = _anchorY + newY;
			
			_shape.graphics.lineTo(x, y);
		}
		
		public function drawCircle(x:Number, y:Number, radius:Number) : void
		{
			x -= _anchorX;
			y -= _anchorY;
			
			var newX:Number = x * _angleCos - y * _angleSin;
			var newY:Number = x * _angleSin + y * _angleCos;
			
			x = _anchorX + newX;
			y = _anchorY + newY;
			
			_shape.graphics.drawCircle(x, y, radius);
		}
		
	}

}