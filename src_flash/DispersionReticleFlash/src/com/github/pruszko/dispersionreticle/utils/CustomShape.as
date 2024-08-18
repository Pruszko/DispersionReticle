package com.github.pruszko.dispersionreticle.utils 
{
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.display.BlendMode;
	import flash.display.LineScaleMode;
	
	public class CustomShape extends Sprite implements Disposable
	{
		
		private var _alphaShape:Shape = new Shape();
		private var _blendShape:Shape = new Shape();
		
		private var _alphaShapeFragment:ShapeFragment = new ShapeFragment(_alphaShape);
		private var _blendShapeFragment:ShapeFragment = new ShapeFragment(_blendShape);
		
		private var _blendStrength:Number = 0.0;
		
		public function CustomShape() 
		{
			this.addChild(_alphaShape);
			this.addChild(_blendShape);
			
			this._alphaShape.alpha = 1.0;
			this._blendShape.blendMode = BlendMode.ADD;
		}
		
		public function disposeState() : void
		{
			this._alphaShapeFragment.disposeState();
			this._alphaShapeFragment = null;
			this.removeChild(_alphaShape);
			this._alphaShape = null;
			
			this._blendShapeFragment.disposeState();
			this._blendShapeFragment = null;
			this.removeChild(_blendShape);
			this._blendShape = null;
		}
		
		public function setBlendStrength(blendStrength:Number) : void
		{
			this._blendStrength = blendStrength;
			this._alphaShape.alpha = 1.0 - blendStrength;
		}
		
		public function setAnchor(anchorX:Number, anchorY:Number) : void
		{
			this._alphaShapeFragment.setAnchor(anchorX, anchorY);
			this._blendShapeFragment.setAnchor(anchorX, anchorY);
		}
		
		public function setAngleDeg(angleDeg:Number) : void
		{
			this._alphaShapeFragment.setAngleDeg(angleDeg);
			this._blendShapeFragment.setAngleDeg(angleDeg);
		}
		
		public function setAngleRad(angleRad:Number) : void
		{
			this._alphaShapeFragment.setAngleRad(angleRad);
			this._blendShapeFragment.setAngleRad(angleRad);
		}
		
		public function clear() : void
		{
			this._alphaShape.graphics.clear();
			this._blendShape.graphics.clear();
		}
		
		public function lineStyle(thickness:Number = -1, color:uint = 0) : void
		{
			if (thickness == -1)
			{
				this._alphaShape.graphics.lineStyle();
				this._blendShape.graphics.lineStyle();
				return;
			}
			
			var blendColor:int = Utils.multiplyColor(color, _blendStrength);
			
			this._alphaShape.graphics.lineStyle(thickness, color, 1.0, false, LineScaleMode.NONE);
			this._blendShape.graphics.lineStyle(thickness, blendColor, 1.0, false, LineScaleMode.NONE);
		}
		
		public function beginFill(color:uint) : void
		{
			var blendColor:int = Utils.multiplyColor(color, _blendStrength);
			
			this._alphaShape.graphics.beginFill(color);
			this._blendShape.graphics.beginFill(blendColor);
		}
		
		public function endFill() : void
		{
			this._alphaShape.graphics.endFill();
			this._blendShape.graphics.endFill();
		}
		
		public function moveTo(x:Number, y:Number) : void
		{
			this._alphaShapeFragment.moveTo(x, y);
			this._blendShapeFragment.moveTo(x, y);
		}
		
		public function lineTo(x:Number, y:Number) : void
		{
			this._alphaShapeFragment.lineTo(x, y);
			this._blendShapeFragment.lineTo(x, y);
		}
		
		public function drawCircle(x:Number, y:Number, radius:Number) : void
		{
			this._alphaShapeFragment.drawCircle(x, y, radius);
			this._blendShapeFragment.drawCircle(x, y, radius);
		}
		
	}

}