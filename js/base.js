class QrCodeRecognition {
	constructor(opts = {}) {
		this.Animation = false ;
		this.timer = null;
		this.video = document.createElement('video');
		this.cvsele = document.querySelector('#canvas');
		this.canvas = this.cvsele.getContext('2d', { willReadFrequently: true });
		this.seuccess = opts.seuccess || Function;
		this.videoTrack=null;
	};
	
	draw(begin, end) {
		this.canvas.beginPath();
		this.canvas.moveTo(begin.x, begin.y);
		this.canvas.lineTo(end.x, end.y);
		this.canvas.lineWidth = 3;
		this.canvas.strokeStyle = 'red';
		this.canvas.stroke();
	};

	cance() {
		this.Animation=false;
		cancelAnimationFrame(this.timer);
		this.cvsele.style.display = "none";
		if(this.videoTrack)	this.videoTrack.forEach(track => track.stop());

	};


	untie() {
		if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
			let { videoWidth, videoHeight } = this.video;
			this.cvsele.width = videoWidth;
			this.cvsele.height = videoHeight;
			this.canvas.drawImage(this.video, 0, 0, videoWidth, videoHeight);

			let img = this.canvas.getImageData(0, 0, videoWidth, videoHeight);
			let obj = jsQR(img.data, img.width, img.height, { inversionAttempts: 'dontInvert' });

			if (obj && this.Animation) {
				let loc = obj.location;
				this.draw(loc.topLeftCorner, loc.topRightCorner);
				this.draw(loc.topRightCorner, loc.bottomRightCorner);
				this.draw(loc.bottomRightCorner, loc.bottomLeftCorner);
				this.draw(loc.bottomLeftCorner, loc.topLeftCorner);

				this.seuccess(obj);
			}
		};
		this.timer = requestAnimationFrame(() => {
			this.untie();
		});

	};
	
	

	sweep() {
		this.Animation=true;
		this.cvsele.style.display = "block";

		navigator.mediaDevices.getUserMedia({
			video: { 
				facingMode: "environment",
				width: { ideal: 1280 },
				height: { ideal: 720 }, 
			}
		}).then (stream => {
			
			this.video.srcObject = stream;
			this.videoTrack = stream.getVideoTracks();  
			this.video.setAttribute('playsinline', true);
			this.video.setAttribute('webkit-playsinline', true);
			//this.video.addEventListener('loadedmetadata', () => {  });
			this.video.play();
			this.untie();
		}).catch  (error => {
			this.cance();
			if (location.origin.indexOf('https://') < 0) 
				alert('因安全性问题，需要在localhost 或 127.0.0.1 或 https 下才能获取权限！');
			else
				alert('对不起：未识别到扫描设备!');
		});
		console.log('sweep fnish');

	};

};


var filename = '';
var filelist = {};
var QrCnt    = 0 ;
var QrSize   = 0 ;
var start,end ;

var result = document.querySelector('#result');
var sweepc = document.querySelector('.sweep');
var h1c    = document.querySelector('.h1');

var QrCode = new QrCodeRecognition({
	
	seuccess: function (res) {

		let parts = res.data.split(':');
		if(parts){
			//parts[3] = parts.slice(3).join(':');
			
			if(filename==parts[0]){
				if(!(parts[1] in filelist)){
					QrCnt ++ ;
					filelist[parts[1]] = parts[3] ;
				}
			}
			else if(parts[3]){
				
				filename  = parts[0];
				QrSize    = parseInt(parts[2]);
				filelist  = {};
				QrCnt     = 1 ;
				filelist[parts[1]] = parts[3] ;
				console.log("NEWFILE",filename);
				h1c.textContent = filename;
			}
			else{
				result.value = '不支持该二维码\n'+res.data;
				return;
			}
			
			let infoData = '当前：'+parts[1]+', 进度：'+(100*QrCnt/QrSize).toFixed(2)+'% ('+QrCnt+'/'+QrSize+')\n剩余：';
			for(var i=0; i<QrSize; i++){
				if(!(i in filelist))
					infoData += i+' ';
			}
			console.log(infoData);
			result.value = infoData;		
			
			if(filename && QrCnt==QrSize){
	
				this.cance();
				let totalData = "";
	
				for(var i=0; i<QrSize; i++){
					totalData += filelist[i] ;
				}

				var binaryString = atob(totalData);
				var len = binaryString.length;  
				var bytes = new Uint8Array(len);  
				for (let i = 0; i < len; i++) {  
					bytes[i] = binaryString.charCodeAt(i);  
				}  
	
				var blob = new Blob([bytes], {type: 'application/octet-stream'});
	
				var downloadLink = document.createElement('a');
				downloadLink.setAttribute('href', window.URL.createObjectURL(blob));
				downloadLink.setAttribute('download', filename);
	
				downloadLink.click();
				downloadLink.remove();
	
				sweepc.textContent ='开扫';	
				
				end = performance.now(); // 记录结束时间 
				let timeElapsed = ((end - start)/1000.0).toFixed(2);
				result.value = filename+"已全部接收\n耗时："+timeElapsed+'s\n平均带宽：'+(len/(end - start)).toFixed(2)+'kB/s';	
				
				filename = '';
				filelist={};
			}
		}
	}
});

function sweep() {
	//console.log(sweepc.textContent);
	if(sweepc.textContent =='开扫'){
		result.value = '';
		QrCode.sweep();
		sweepc.textContent ='暂停';
		start = performance.now(); 
	}
	else if(sweepc.textContent =='暂停'){
		QrCode.cance();
		sweepc.textContent ='继续';
	}
	else if(sweepc.textContent =='继续'){
		QrCode.sweep();
		sweepc.textContent ='暂停';
	}
};
