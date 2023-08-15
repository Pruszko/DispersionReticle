package com.github.pruszko.dispersionreticle.utils 
{
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class DisposableCustomShape extends Sprite implements Disposable
	{
		
		private var _alphaShape:Shape = new Shape();
		private var _blendShape:Shape = new Shape();
		
		private var _alphaShapeFragment:DisposableShapeFragment = new DisposableShapeFragment(_alphaShape);
		private var _blendShapeFragment:DisposableShapeFragment = new DisposableShapeFragment(_blendShape);
		
		private var _blendStrength:Number = 0.0;
		
		public function DisposableCustomShape() 
		{
			addChild(_alphaShape);
			addChild(_blendShape);
			
			_alphaShape.alpha = 1.0;
			_blendShape.blendMode = BlendMode.ADD;
		}
		
		public function disposeState() : void
		{
			_alphaShapeFragment.disposeState();
			_alphaShapeFragment = null;
			removeChild(_alphaShape);
			this._alphaShape = null;
			
			_blendShapeFragment.disposeState();
			_blendShapeFragment = null;
			removeChild(_blendShape);
			this._blendShape = null;
		}
		
		public function setBlendStrength(blendStrength:Number) : void
		{
			this._blendStrength = blendStrength;
			_alphaShape.alpha = 1.0 - blendStrength;
		}
		
		public function setAnchor(anchorX:Number, anchorY:Number) : void
		{
			_alphaShapeFragment.setAnchor(anchorX, anchorY);
			_blendShapeFragment.setAnchor(anchorX, anchorY);
		}
		
		public function setAngleDeg(angleDeg:Number) : void
		{
			_alphaShapeFragment.setAngleDeg(angleDeg);
			_blendShapeFragment.setAngleDeg(angleDeg);
		}
		
		public function setAngleRad(angleRad:Number) : void
		{
			_alphaShapeFragment.setAngleRad(angleRad);
			_blendShapeFragment.setAngleRad(angleRad);
		}
		
		public function clear() : void
		{
			_alphaShape.graphics.clear();
			_blendShape.graphics.clear();
		}
		
		public function lineStyle(thickness:Number = -1, color:uint = 0) : void
		{
			if (thickness == -1)
			{
				_alphaShape.graphics.lineStyle();
				_blendShape.graphics.lineStyle();
				return;
			}
			
			var blendColor:int = Utils.multiplyColor(color, _blendStrength);
			
			_alphaShape.graphics.lineStyle(thickness, color, 1.0, false, LineScaleMode.NONE);
			_blendShape.graphics.lineStyle(thickness, blendColor, 1.0, false, LineScaleMode.NONE);
		}
		
		public function beginFill(color:uint) : void
		{
			var blendColor:int = Utils.multiplyColor(color, _blendStrength);
			
			_alphaShape.graphics.beginFill(color);
			_blendShape.graphics.beginFill(blendColor);
		}
		
		public function endFill() : void
		{
			_alphaShape.graphics.endFill();
			_blendShape.graphics.endFill();
		}
		
		public function moveTo(x:Number, y:Number) : void
		{
			_alphaShapeFragment.moveTo(x, y);
			_blendShapeFragment.moveTo(x, y);
		}
		
		public function lineTo(x:Number, y:Number) : void
		{
			_alphaShapeFragment.lineTo(x, y);
			_blendShapeFragment.lineTo(x, y);
		}
		
		public function drawCircle(x:Number, y:Number, radius:Number) : void
		{
			_alphaShapeFragment.drawCircle(x, y, radius);
			_blendShapeFragment.drawCircle(x, y, radius);
		}
		
	}

}