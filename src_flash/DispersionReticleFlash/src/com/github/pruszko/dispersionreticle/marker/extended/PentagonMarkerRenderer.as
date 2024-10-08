package com.github.pruszko.dispersionreticle.marker.extended 
{
	import com.github.pruszko.dispersionreticle.marker.ExtendedMarker;
	
	public class PentagonMarkerRenderer extends MarkerRenderer
	{
		
		private var _elementWidth:Number = 0.0;
		private var _elementHeight:Number = 0.0;
				
		private var _circleRadius:Number = 0.0;
		
		public function PentagonMarkerRenderer(extendedMarker:ExtendedMarker) 
		{
			super(extendedMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			this._elementWidth = this.scaleSqrtByReticleRadius(1.0 * this.config.shapes.pentagon.width);
			this._elementHeight = this.scaleSqrtByReticleRadius(1.0 * this.config.shapes.pentagon.height);
			
			this._circleRadius = this.scaleSqrtByReticleRadius(0.25 * this.config.centerDotSize);
		}
		
		override public function renderState() : void
		{
			super.renderState();
			
			if (this.config.centerDotSize > 0.01)
			{
				this.drawCenter();
			}
			
			for (var i:int = 0; i < 4; ++i)
			{
				this.shape.setAngleDeg(i * 90.0);
				this.outlineShape.setAngleDeg(i * 90.0);
				
				this.drawRotatedTopPentagon();
				
				if (this.config.drawOutline)
				{
					this.drawRotatedTopPentagonOutline();
				}
			}
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
		
		private function drawRotatedTopPentagon() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -this.reticleRadius;
			
			this.shape.lineStyle();
			this.shape.beginFill(this.config.color);
			
			this.shape.moveTo(posX - this._elementWidth, posY - this._elementHeight);
			this.shape.lineTo(posX + this._elementWidth, posY - this._elementHeight);
			this.shape.lineTo(posX + this._elementWidth, posY);
			this.shape.lineTo(posX, posY + this._elementHeight);
			this.shape.lineTo(posX - this._elementWidth, posY);
			this.shape.lineTo(posX - this._elementWidth, posY - this._elementHeight);
			
			this.shape.graphics.endFill();
		}
		
		private function drawRotatedTopPentagonOutline() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -this.reticleRadius;
			
			this.outlineShape.lineStyle(1.0, 0x000000);
			
			this.outlineShape.moveTo(posX - this._elementWidth, posY - this._elementHeight);
			this.outlineShape.lineTo(posX + this._elementWidth, posY - this._elementHeight);
			this.outlineShape.lineTo(posX + this._elementWidth, posY);
			this.outlineShape.lineTo(posX, posY + this._elementHeight);
			this.outlineShape.lineTo(posX - this._elementWidth, posY);
			this.outlineShape.lineTo(posX - this._elementWidth, posY - this._elementHeight);
		}
		
	}

}