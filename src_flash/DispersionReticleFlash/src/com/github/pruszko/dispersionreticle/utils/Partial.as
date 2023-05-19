package com.github.pruszko.dispersionreticle.utils 
{
	import flash.utils.getTimer;
	
	public class Partial 
	{
		
		private var partialValues:Vector.<PartialValue> = new Vector.<PartialValue>();
		
		private var lastTimeMilliseconds:int = getTimer();
		private var tickMilliseconds:Number;
		
		private var partialScale:Number = 1.0;
		
		public function Partial(tickMilliseconds:Number) 
		{
			super();
			
			this.tickMilliseconds = tickMilliseconds;
		}
		
		internal function append(partialValue:PartialValue) : void
		{
			this.partialValues.push(partialValue);
		}
		
		public function reset() : void
		{
			this.lastTimeMilliseconds = getTimer();
			
			for (var i:int = 0; i < this.partialValues.length; i++)
			{
				this.partialValues[i].reset();
			}
		}
		
		public function tick() : void
		{
			var diffInMilliseconds:Number = getTimer() - this.lastTimeMilliseconds;
			
			this.partialScale = diffInMilliseconds / this.tickMilliseconds;
			if (this.partialScale >= 1.0)
			{
				this.partialScale = 1.0;
			}
		}
		
		public function interpolate(prevValue:Number, value:Number) : Number
		{
			return prevValue + value * partialScale - prevValue * partialScale;
		}
		
	}

}