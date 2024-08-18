package com.github.pruszko.dispersionreticle.utils 
{
	import flash.utils.getTimer;
	
	public class Partial implements Disposable
	{
		
		private var _partialValues:Vector.<PartialValue> = new Vector.<PartialValue>();
		
		private var _lastTimeMilliseconds:int = getTimer();
		private var _tickMilliseconds:Number;
		
		private var _partialScale:Number = 1.0;
		
		public function Partial(tickMilliseconds:Number) 
		{
			super();
			
			this._tickMilliseconds = tickMilliseconds;
		}
		
		public function disposeState() : void
		{
			for (var i:int = 0; i < this._partialValues.length; ++i)
			{
				this._partialValues[i].disposeState();
			}
			
			this._partialValues.splice(0, this._partialValues.length);
			this._partialValues = null;
		}
		
		internal function append(partialValue:PartialValue) : void
		{
			this._partialValues.push(partialValue);
		}
		
		public function reset() : void
		{
			this._lastTimeMilliseconds = getTimer();
			
			for (var i:int = 0; i < this._partialValues.length; i++)
			{
				this._partialValues[i].reset();
			}
		}
		
		public function tick() : void
		{
			var diffInMilliseconds:Number = getTimer() - this._lastTimeMilliseconds;
			
			this._partialScale = diffInMilliseconds / this._tickMilliseconds;
			if (this._partialScale >= 1.0)
			{
				this._partialScale = 1.0;
			}
		}
		
		public function interpolate(prevValue:Number, value:Number) : Number
		{
			return prevValue + value * this._partialScale - prevValue * this._partialScale;
		}
		
	}

}