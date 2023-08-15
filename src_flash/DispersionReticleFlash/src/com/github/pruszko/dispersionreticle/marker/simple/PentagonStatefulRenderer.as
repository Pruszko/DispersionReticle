package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.marker.SimpleStatefulMarker;
	
	public class PentagonStatefulRenderer extends StatefulRenderer
	{
		
		private var _elementScale:Number = 0.0;
		private var _circleRadius:Number = 0.0;
		
		public function PentagonStatefulRenderer(simpleMarker:SimpleStatefulMarker) 
		{
			super(simpleMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			_elementScale = scaleLogByReticleRadius(3.0);
			_circleRadius = scaleLogByReticleRadius(1.0);
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			for (var i:int = 0; i < 4; ++i)
			{
				shape.setAngleDeg(i * 90.0);
				outlineShape.setAngleDeg(i * 90.0);
				
				drawRotatedTopPentagon();
				
				if (shouldDrawOutline)
				{
					drawRotatedTopPentagonOutline();
				}
			}
			
			drawCenterCircle();
			
			if (shouldDrawOutline)
			{
				outlineShape.setAngleDeg(0.0);
				
				drawCenterCircleOutline();
			}
		}
		
		private function drawRotatedTopPentagon() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -reticleRadius;
			
			shape.lineStyle();
			shape.beginFill(fillColor);
			
			shape.moveTo(posX - _elementScale, posY - _elementScale);
			shape.lineTo(posX + _elementScale, posY - _elementScale);
			shape.lineTo(posX + _elementScale, posY);
			shape.lineTo(posX, posY + _elementScale);
			shape.lineTo(posX - _elementScale, posY);
			shape.lineTo(posX - _elementScale, posY - _elementScale);
			
			shape.graphics.endFill();
		}
		
		private function drawRotatedTopPentagonOutline() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -reticleRadius;
			
			outlineShape.lineStyle(1.0, 0x000000);
			
			outlineShape.moveTo(posX - _elementScale, posY - _elementScale);
			outlineShape.lineTo(posX + _elementScale, posY - _elementScale);
			outlineShape.lineTo(posX + _elementScale, posY);
			outlineShape.lineTo(posX, posY + _elementScale);
			outlineShape.lineTo(posX - _elementScale, posY);
			outlineShape.lineTo(posX - _elementScale, posY - _elementScale);
		}
		
		private function drawCenterCircle() : void
		{
			shape.lineStyle();
			shape.beginFill(fillColor);
			
			shape.drawCircle(0.0, 0.0, _circleRadius);
			
			shape.endFill();
		}
		
		private function drawCenterCircleOutline() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			outlineShape.lineStyle(1.0, 0x000000);
			outlineShape.drawCircle(centerX, centerY, _circleRadius);
		}
		
	}

}