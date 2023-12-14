package com.github.pruszko.dispersionreticle.utils 
{

	public class GunMarkerTypes 
	{
		
		public static const FOCUSED_EXTENDED_CLIENT:int = 7;
		public static const FOCUSED_EXTENDED_SERVER:int = 8;
		public static const HYBRID_EXTENDED_CLIENT:int = 9;
		public static const SERVER_EXTENDED_SERVER:int = 10;
		
		public static function isCustomReticle(gunMarkerType:int) : Boolean
		{
			return gunMarkerType >= 7 && gunMarkerType <= 10;
		}
		
	}

}