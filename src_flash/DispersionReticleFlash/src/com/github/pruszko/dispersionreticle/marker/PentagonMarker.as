package com.github.pruszko.dispersionreticle.marker 
{
	import com.github.pruszko.dispersionreticle.DispersionReticleFlash;
	import flash.display.Shape;
	import flash.display.Sprite;
	
	public class PentagonMarker extends Sprite
	{
		
		private static const PENTAGON_RADIUS_SCALE:Number = 0.004;
		
		private var app:DispersionReticleFlash;
		
		private var shape:Shape = new Shape();
		public var isOnScreen:Boolean = true;
		
		private var pentagonRadius:Number = 0.0;
		
		public function PentagonMarker(app:DispersionReticleFlash)
		{
			super();
			
			this.app = app
			
			addChild(shape);
		}
		
		public function draw(reticleSize:Number) : void
		{
			recalculatePentagonSize();
			
			shape.graphics.clear()
			
			if (!isOnScreen) {
				return;
			}
			
			drawPentagonTop(reticleSize);
			drawPentagonRight(reticleSize);
			drawPentagonBottom(reticleSize);
			drawPentagonLeft(reticleSize);
			drawPentagonCenter();
		}
		
		private function recalculatePentagonSize() : void
		{
			pentagonRadius = PENTAGON_RADIUS_SCALE * app.appHeight;
			if (app.appWidth < app.appHeight)
			{
				pentagonRadius = PENTAGON_RADIUS_SCALE * app.appWidth;
			}
		}
		
		private function drawPentagonTop(reticleSize:Number) : void
		{
			shape.graphics.beginFill(app.fillColor);
			
			var centerX:Number = 0.0;
			var centerY:Number = 0.0 - reticleSize;
			shape.graphics.moveTo(centerX - pentagonRadius, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY);
			shape.graphics.lineTo(centerX, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY - pentagonRadius);
			
			shape.graphics.endFill();
		}
		
		private function drawPentagonRight(reticleSize:Number) : void
		{
			shape.graphics.beginFill(app.fillColor);
			
			var centerX:Number = 0.0 + reticleSize;
			var centerY:Number = 0.0;
			shape.graphics.moveTo(centerX, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY);
			shape.graphics.lineTo(centerX, centerY - pentagonRadius);
			
			shape.graphics.endFill();
		}
		
		private function drawPentagonBottom(reticleSize:Number) : void
		{
			shape.graphics.beginFill(app.fillColor);
			
			var centerX:Number = 0.0;
			var centerY:Number = 0.0 + reticleSize;
			shape.graphics.moveTo(centerX, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY);
			shape.graphics.lineTo(centerX, centerY - pentagonRadius);
			
			shape.graphics.endFill();
		}
		
		private function drawPentagonLeft(reticleSize:Number) : void
		{
			shape.graphics.beginFill(app.fillColor);
			
			var centerX:Number = 0.0 - reticleSize;
			var centerY:Number = 0.0;
			shape.graphics.moveTo(centerX - pentagonRadius, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX, centerY - pentagonRadius);
			shape.graphics.lineTo(centerX + pentagonRadius, centerY);
			shape.graphics.lineTo(centerX, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY + pentagonRadius);
			shape.graphics.lineTo(centerX - pentagonRadius, centerY - pentagonRadius);
			
			shape.graphics.endFill();
		}
		
		private function drawPentagonCenter() : void
		{
			shape.graphics.beginFill(app.fillColor);
			
			shape.graphics.drawCircle(0.0, 0.0, pentagonRadius);
			
			shape.graphics.endFill();
		}
		
	}

}