package com.github.pruszko.dispersionreticle.utils 
{
	
	public interface Stateful extends Disposable
	{
		function updateState() : void;
		function renderState() : void;
	}
	
}