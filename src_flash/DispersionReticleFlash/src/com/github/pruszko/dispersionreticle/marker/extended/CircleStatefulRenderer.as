package com.github.pruszko.dispersionreticle.marker.extended 
{
	import com.github.pruszko.dispersionreticle.marker.ExtendedStatefulMarker;
	
	public class CircleStatefulRenderer extends StatefulRenderer
	{
		
		private var _circleRadius:Number = 0.0;
		
		public function CircleStatefulRenderer(extendedMarker:ExtendedStatefulMarker) 
		{
			super(extendedMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			this._circleRadius = scaleSqrtByReticleRadius(0.25 * this.config.centerDotSize);
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			this.drawReticle();
			
			if (this.config.centerDotSize > 0.01)
			{
				this.drawCenter();
			}
			
			if (this.config.drawOutline)
			{
				this.drawReticleOutline();
			}
		}
		
		private function drawReticle() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			this.shape.lineStyle(1.0, this.config.color);
			this.shape.drawCircle(centerX, centerY, this.reticleRadius);
		}
		
		private function drawCenter() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			this.shape.lineStyle();
			this.shape.beginFill(this.config.color);
			
			this.shape.drawCircle(centerX, centerY, this._circleRadius);
			
			this.shape.endFill();
		}
		
		private function drawReticleOutline() : void
		{
			var centerX:Number = 0.0;
			var centerY:Number = 0.0;
			
			this.outlineShape.lineStyle(1.0, 0x000000);
			this.outlineShape.drawCircle(centerX, centerY, this.reticleRadius + 1.0);
		}
		
	}

}