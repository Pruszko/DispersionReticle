package com.github.pruszko.dispersionreticle.utils 
{

	public class GunMarkerTypes 
	{
		
		public static const FOCUSED_EXTENDED_CLIENT:int = 8;
		public static const FOCUSED_EXTENDED_SERVER:int = 9;
		public static const HYBRID_EXTENDED_CLIENT:int = 10;
		public static const SERVER_EXTENDED_SERVER:int = 11;
		
		public static function isCustomReticle(gunMarkerType:int) : Boolean
		{
			return gunMarkerType >= 8 && gunMarkerType <= 11;
		}
		
	}

}