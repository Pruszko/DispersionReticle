package com.github.pruszko.dispersionreticle.marker.extended 
{
	import com.github.pruszko.dispersionreticle.marker.ExtendedStatefulMarker;
	
	public class TShapeStatefulRenderer extends StatefulRenderer
	{
		
		private var _elementThickness:Number = 0.0;
		private var _elementLength:Number = 0.0;
		
		private var _circleRadius:Number = 0.0;
		
		public function TShapeStatefulRenderer(extendedMarker:ExtendedStatefulMarker) 
		{
			super(extendedMarker);
		}
		
		override public function updateState() : void
		{
			super.updateState();
			
			var inversion:Number = this.config.shapes.tshape.length >= 0.0 ? 1.0 : -1.0;
			
			this._elementThickness = this.scaleSqrtByReticleRadius(0.5 * inversion * this.config.shapes.tshape.thickness);
			this._elementLength = this.scaleSqrtByReticleRadius(1.0 * this.config.shapes.tshape.length);
			
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
				
				this.drawRotatedTopTShape();
				
				if (this.config.drawOutline)
				{
					this.drawRotatedTopTShapeOutline();
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
		
		private function drawRotatedTopTShape() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -this.reticleRadius;
			
			this.shape.lineStyle();
			this.shape.beginFill(this.config.color);
			
			this.shape.moveTo(posX - this._elementThickness - this._elementLength, posY - this._elementThickness);
			this.shape.lineTo(posX + this._elementThickness + this._elementLength, posY - this._elementThickness);
			this.shape.lineTo(posX + this._elementThickness + this._elementLength, posY + this._elementThickness);
			this.shape.lineTo(posX + this._elementThickness, posY + this._elementThickness);
			this.shape.lineTo(posX + this._elementThickness, posY + this._elementThickness + this._elementLength);
			this.shape.lineTo(posX - this._elementThickness, posY + this._elementThickness + this._elementLength);
			this.shape.lineTo(posX - this._elementThickness, posY + this._elementThickness);
			this.shape.lineTo(posX - this._elementThickness - this._elementLength, posY + this._elementThickness);
			this.shape.lineTo(posX - this._elementThickness - this._elementLength, posY - this._elementThickness);
			
			this.shape.endFill();
		}
		
		private function drawRotatedTopTShapeOutline() : void
		{
			var posX:Number = 0.0;
			var posY:Number = -this.reticleRadius;
			
			this.outlineShape.lineStyle(1.0, 0x000000);
			
			this.outlineShape.moveTo(posX - this._elementThickness - this._elementLength, posY - this._elementThickness);
			this.outlineShape.lineTo(posX + this._elementThickness + this._elementLength, posY - this._elementThickness);
			this.outlineShape.lineTo(posX + this._elementThickness + this._elementLength, posY + this._elementThickness);
			this.outlineShape.lineTo(posX + this._elementThickness, posY + this._elementThickness);
			this.outlineShape.lineTo(posX + this._elementThickness, posY + this._elementThickness + this._elementLength);
			this.outlineShape.lineTo(posX - this._elementThickness, posY + this._elementThickness + this._elementLength);
			this.outlineShape.lineTo(posX - this._elementThickness, posY + this._elementThickness);
			this.outlineShape.lineTo(posX - this._elementThickness - this._elementLength, posY + this._elementThickness);
			this.outlineShape.lineTo(posX - this._elementThickness - this._elementLength, posY - this._elementThickness);
		}
		
	}

}