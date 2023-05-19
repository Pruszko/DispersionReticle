package com.github.pruszko.dispersionreticle.utils 
{
	import com.github.pruszko.dispersionreticle.utils.Partial;
	
	public class PartialValue 
	{

		private var parentPartial:Partial;
		
		private var prevValue:Number;
		public var value:Number;
		
		public function PartialValue(parentPartial:Partial, value:Number = 0.0)
		{
			super();
			
			this.parentPartial = parentPartial;
			this.prevValue = value;
			this.value = value;
			
			parentPartial.append(this);
		}
		
		internal function reset() : void
		{
			this.prevValue = this.value;
		}
		
		public function get partial() : Number
		{
			return parentPartial.interpolate(prevValue, value);
		}
		
	}

}