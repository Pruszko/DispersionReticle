package com.github.pruszko.dispersionreticle.marker.simple 
{
	import com.github.pruszko.dispersionreticle.marker.SimpleStatefulMarker;
	
	public class CircleStatefulRenderer extends StatefulRenderer
	{
		
		// Purposedly add few pixels not to hide solid circle reticle while reloading
		private static const SPACE_FOR_RELOAD:Number = 3.0;
		
		public function CircleStatefulRenderer(simpleMarker:SimpleStatefulMarker) 
		{
			super(simpleMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			drawReticle();
			
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
			shape.drawCircle(centerX, centerY, reticleRadius + SPACE_FOR_RELOAD);
		}
		
		private function drawReticleOutline() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			outlineShape.lineStyle(1.0, 0x000000);
			outlineShape.drawCircle(centerX, centerY, reticleRadius + SPACE_FOR_RELOAD + 1.0);
		}
		
	}

}