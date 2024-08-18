package com.github.pruszko.dispersionreticle.utils 
{

	public class ReticleTypes
	{
		
		public static const FOCUSED_EXTENDED:int = 5;
		public static const HYBRID_EXTENDED:int = 6;
		public static const SERVER_EXTENDED:int = 7;
		
		public static function isExtendedReticle(reticleId:int) : Boolean
		{
			return reticleId >= 5 && reticleId <= 7;
		}
		
	}

}