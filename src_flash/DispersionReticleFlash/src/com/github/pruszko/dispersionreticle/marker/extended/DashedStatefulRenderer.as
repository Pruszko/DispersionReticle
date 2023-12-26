package com.github.pruszko.dispersionreticle.marker.extended 
{
	import com.github.pruszko.dispersionreticle.marker.ExtendedStatefulMarker;
	import com.github.pruszko.dispersionreticle.utils.Utils;
	
	public class DashedStatefulRenderer extends StatefulRenderer
	{
		
		private var _halfDashWidth:Number = 0.0;
		private var _halfDashHeight:Number = 0.0;
		private var _lineThickness:Number = 0.0;
		private var _innerFillColor:int = 0x000000;
		
		private var _circleRadius:Number = 0.0;
		
		public function DashedStatefulRenderer(extendedMarker:ExtendedStatefulMarker) 
		{
			super(extendedMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			var dashHeight:Number = this.reticleRadius / 20.0;
			
			this._halfDashHeight = dashHeight / 2.0;
			this._halfDashWidth = this._halfDashHeight * 5.0 / 16.0;
			this._lineThickness = this._halfDashWidth / 2.0;
			this._innerFillColor = Utils.multiplyColor(config.color, 0.6);
			
			this._circleRadius = this.scaleSqrtByReticleRadius(0.25);
		}
		
		override public function renderState() : void
		{
			super.renderState();
						
			for (var i:int = 0; i < 36; ++i)
			{
				// dashed reticle does not starts exactly at top
				// it's like partitioned by 9 dashed in each quarter
				this.shape.setAngleDeg(5.0 + i * 10.0);
				
				this.drawRotatedTopDash();
			}
			
			if (this.config.drawCenterDot)
			{
				this.drawCenter();
			}
						
			if (this.config.drawOutline)
			{
				this.outlineShape.setAngleDeg(0.0);
				
				this.drawReticleOutline();
			}
		}
		
		private function drawRotatedTopDash() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -this.reticleRadius;
			
			this.shape.lineStyle(this._lineThickness, this.config.color);
			this.shape.beginFill(this._innerFillColor);
			
			this.shape.moveTo(posX - this._halfDashWidth, posY - this._halfDashHeight);
			this.shape.lineTo(posX + this._halfDashWidth, posY - this._halfDashHeight);
			this.shape.lineTo(posX + this._halfDashWidth, posY + this._halfDashHeight);
			this.shape.lineTo(posX - this._halfDashWidth, posY + this._halfDashHeight);
			this.shape.lineTo(posX - this._halfDashWidth, posY - this._halfDashHeight);
			
			this.shape.endFill();
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
			
			// Add few minimum pixels not to hide solid circle reticle while reloading
			var outlineSpace:Number = this._halfDashHeight > 1.0 ? this._halfDashHeight : 1.0;
			
			this.outlineShape.lineStyle(1.0, 0x000000);
			this.outlineShape.drawCircle(centerX, centerY, this.reticleRadius + outlineSpace);
		}
		
	}

}