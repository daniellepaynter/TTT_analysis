/*
 * Macro template to merge GFP and TOM images in a folder
 */

#@ File (label = "Input directory", style = "directory") input_big

findFolders(input_big);

function findFolders(input_big) {
	list = getFileList(input_big);
	// list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		print(list[i]);
		if(File.isDirectory(input_big + File.separator + list[i]))
			processFolder(input_big + File.separator + list[i]);
		
		
	}
}


function processFolder(source_dir) {
	output = "F:\iLastik" + File.separator + list[i] + File.separator;
	File.makeDirectory(output);
	GFP=source_dir+File.separator+"GFP"+File.separator;
	print(GFP);
	File.openSequence(GFP)
	TOM=source_dir+File.separator+"TOM"+File.separator;
	File.openSequence(TOM)
	run("Merge Channels...", "c1=TOM c2=GFP create");
	selectWindow("Composite");
	run("RGB Color", "slices");
	run("Image Sequence... ", "select="+output+ "dir="+output+" format=TIFF digits=2 use");
	print('Did a thing');
	close();
}

