package com.github.pruszko.dispersionreticle.utils 
{
	import com.github.pruszko.dispersionreticle.utils.DisposablePartial;
	
	public class DisposablePartialValue implements Disposable 
	{

		private var _parentPartial:DisposablePartial;
		
		private var _prevValue:Number;
		public var value:Number;
		
		public function DisposablePartialValue(parentPartial:DisposablePartial, value:Number = 0.0)
		{
			super();
			
			this._parentPartial = parentPartial;
			this._prevValue = value;
			this.value = value;
			
			parentPartial.append(this);
		}
		
		public function disposeState() : void
		{
			this._parentPartial = null;
		}
		
		internal function reset() : void
		{
			this._prevValue = this.value;
		}
		
		public function get partial() : Number
		{
			return _parentPartial.interpolate(_prevValue, value);
		}
		
	}

}