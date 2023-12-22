package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.marker.CustomStatefulMarker;
	
	public class CircleStatefulRenderer extends StatefulRenderer
	{
		
		private var _circleRadius:Number = 0.0;
		
		public function CircleStatefulRenderer(simpleMarker:CustomStatefulMarker) 
		{
			super(simpleMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			_circleRadius = scaleLogByReticleRadius(0.75);
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			drawReticle();
			
			if (shouldDrawCenterDot)
			{
				drawCenter();
			}
			
			if (shouldDrawOutline)
			{
				drawReticleOutline();
			}
		}
		
		private function drawReticle() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			shape.lineStyle(1.0, fillColor);
			shape.drawCircle(centerX, centerY, reticleRadius);
		}
		
		private function drawCenter() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			shape.lineStyle();
			shape.beginFill(fillColor);
			
			shape.drawCircle(centerX, centerY, _circleRadius);
			
			shape.endFill();
		}
		
		private function drawReticleOutline() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			outlineShape.lineStyle(1.0, 0x000000);
			outlineShape.drawCircle(centerX, centerY, reticleRadius + 1.0);
		}
		
	}

}