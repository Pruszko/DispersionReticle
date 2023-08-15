package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.marker.SimpleStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.Utils;
	
	public class DashedStatefulRenderer extends StatefulRenderer
	{
		
		private var _halfDashWidth:Number = 0.0;
		private var _halfDashHeight:Number = 0.0;
		private var _lineThickness:Number = 0.0;
		private var _innerFillColor:int = 0x000000;
		
		private var _circleRadius:Number = 0.0;
		
		public function DashedStatefulRenderer(simpleMarker:SimpleStatefulMarker) 
		{
			super(simpleMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			var dashHeight:Number = reticleRadius / 20.0;
			
			_halfDashHeight = dashHeight / 2.0;
			_halfDashWidth = _halfDashHeight * 5.0 / 16.0;
			_lineThickness = _halfDashWidth / 2.0;
			_innerFillColor = Utils.multiplyColor(fillColor, 0.6);
			
			_circleRadius = scaleLogByReticleRadius(1.0);
		}
		
		override public function renderState() : void
		{
			super.renderState();
						
			for (var i:int = 0; i < 36; ++i)
			{
				// dashed reticle does not starts exactly at top
				// it's like partitioned by 9 dashed in each quarter
				shape.setAngleDeg(5.0 + i * 10.0);
				
				drawRotatedTopDash();
			}
			
			drawCenterCircle();
			
			if (shouldDrawOutline)
			{
				outlineShape.setAngleDeg(0.0);
				
				drawCenterCircleOutline();
				drawReticleOutline();
			}
		}
		
		private function drawRotatedTopDash() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -reticleRadius;
			
			shape.lineStyle(_lineThickness, fillColor);
			shape.beginFill(_innerFillColor);
			
			shape.moveTo(posX - _halfDashWidth, posY - _halfDashHeight);
			shape.lineTo(posX + _halfDashWidth, posY - _halfDashHeight);
			shape.lineTo(posX + _halfDashWidth, posY + _halfDashHeight);
			shape.lineTo(posX - _halfDashWidth, posY + _halfDashHeight);
			shape.lineTo(posX - _halfDashWidth, posY - _halfDashHeight);
			
			shape.endFill();
		}
		
		private function drawReticleOutline() : void
		{	
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			// Add few minimum pixels not to hide solid circle reticle while reloading
			var outlineSpace:Number = _halfDashHeight > 3.0 ? _halfDashHeight : 3.0;
			
			outlineShape.lineStyle(1.0, 0x000000);
			outlineShape.drawCircle(centerX, centerY, reticleRadius + outlineSpace);
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