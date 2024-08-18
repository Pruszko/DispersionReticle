package com.github.pruszko.dispersionreticle.utils 
{
	import com.github.pruszko.dispersionreticle.utils.Partial;
	
	public class PartialValue implements Disposable 
	{

		private var _parentPartial:Partial;
		
		private var _prevValue:Number;
		public var value:Number;
		
		public function PartialValue(parentPartial:Partial, value:Number = 0.0)
		{
			super();
			
			this._parentPartial = parentPartial;
			this._prevValue = value;
			this.value = value;
			
			this._parentPartial.append(this);
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
			return this._parentPartial.interpolate(this._prevValue, this.value);
		}
		
	}

}