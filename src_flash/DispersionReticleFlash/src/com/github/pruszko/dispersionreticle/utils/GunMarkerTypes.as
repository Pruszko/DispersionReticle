package com.github.pruszko.dispersionreticle.utils 
{

	public class GunMarkerTypes 
	{
		
		public static const CUSTOM_FOCUSED_CLIENT:int = 7;
		public static const CUSTOM_FOCUSED_SERVER:int = 8;
		public static const CUSTOM_HYBRID_CLIENT:int = 9;
		public static const CUSTOM_SERVER_SERVER:int = 10;
		
		public static function isCustomReticle(gunMarkerType:int) : Boolean
		{
			return gunMarkerType >= 7 && gunMarkerType <= 10;
		}
		
	}

}