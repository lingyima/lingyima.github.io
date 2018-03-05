var Stack = function(){
	return {
		// item
		items: [],

		// push
		push: function(ele){
			this.items.push(ele)
		},

		// pop
		pop: function(){
			return this.items.pop()
		},

		// top
		top: function() {
			return this.items[this.items.length-1];
		},

		// bottom
		bottom: function(){
			return this.items[0];
		},

		// size
		size: function() {
			return this.items.length;
		},

		// clear
		clear: function() {
			this.items = [];
		},

		// isEmpty
		isEmpty: function() {
			return this.items.length === 0;
		},
		
		stdout: function() {
			return this.items.toString();
		}
	}
};