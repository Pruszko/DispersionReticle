package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.marker.SimpleStatefulMarker;
	
	public class TShapeStatefulRenderer extends StatefulRenderer
	{
		
		private var _elementThickness:Number = 0.0;
		private var _elementLength:Number = 0.0;
		private var _circleRadius:Number = 0.0;
		
		public function TShapeStatefulRenderer(simpleMarker:SimpleStatefulMarker) 
		{
			super(simpleMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			_elementThickness = scaleLogByReticleRadius(1.5);
			_elementLength = scaleLogByReticleRadius(4.0);
			_circleRadius = scaleLogByReticleRadius(1.0);
		}
		
		override public function renderState() : void
		{
			super.renderState();
						
			for (var i:int = 0; i < 4; ++i)
			{
				shape.setAngleDeg(i * 90.0);
				outlineShape.setAngleDeg(i * 90.0);
				
				drawRotatedTopTShape();
				
				if (shouldDrawOutline)
				{
					drawRotatedTopTShapeOutline();
				}
			}
			
			drawCenterCircle();
			
			if (shouldDrawOutline)
			{
				outlineShape.setAngleDeg(0.0);
				
				drawCenterCircleOutline();
			}
		}
		
		private function drawRotatedTopTShape() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -reticleRadius;
			
			shape.lineStyle();
			shape.beginFill(fillColor);
			
			shape.moveTo(posX - _elementLength, posY - _elementThickness);
			shape.lineTo(posX + _elementLength, posY - _elementThickness);
			shape.lineTo(posX + _elementLength, posY + _elementThickness);
			shape.lineTo(posX + _elementThickness, posY + _elementThickness);
			shape.lineTo(posX + _elementThickness, posY + _elementLength);
			shape.lineTo(posX - _elementThickness, posY + _elementLength);
			shape.lineTo(posX - _elementThickness, posY + _elementThickness);
			shape.lineTo(posX - _elementLength, posY + _elementThickness);
			shape.lineTo(posX - _elementLength, posY - _elementThickness);
			
			shape.endFill();
		}
		
		private function drawRotatedTopTShapeOutline() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -reticleRadius;
			
			outlineShape.lineStyle(1.0, 0x000000);
			
			outlineShape.moveTo(posX - _elementLength, posY - _elementThickness);
			outlineShape.lineTo(posX + _elementLength, posY - _elementThickness);
			outlineShape.lineTo(posX + _elementLength, posY + _elementThickness);
			outlineShape.lineTo(posX + _elementThickness, posY + _elementThickness);
			outlineShape.lineTo(posX + _elementThickness, posY + _elementLength);
			outlineShape.lineTo(posX - _elementThickness, posY + _elementLength);
			outlineShape.lineTo(posX - _elementThickness, posY + _elementThickness);
			outlineShape.lineTo(posX - _elementLength, posY + _elementThickness);
			outlineShape.lineTo(posX - _elementLength, posY - _elementThickness);
		}
		
		private function drawCenterCircle() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			shape.lineStyle();
			shape.beginFill(fillColor);
			
			shape.drawCircle(centerX, centerY, _circleRadius);
			
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