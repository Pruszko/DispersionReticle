package com.github.pruszko.dispersionreticle.utils 
{
	
	public class Utils 
	{
		
		public static function multiplyColor(color:uint, scale:Number) : uint
		{
			var r:int = int(((color & 0xFF0000) >> 16) * scale)
			var g:int = int(((color & 0x00FF00) >> 8) * scale)
			var b:int = int((color & 0x0000FF) * scale)
			
			return (r << 16) | (g << 8) | b;
		}
		
	}

}