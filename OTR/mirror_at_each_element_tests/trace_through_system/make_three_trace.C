void set_plot_style()
{
    gROOT->ForceStyle();
    const Int_t NRGBs = 5;
    const Int_t NCont = 255;
    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
}

void macro1(int inpt)
{
	//COLZ scheme
	set_plot_style();
	TCanvas* c = new TCanvas("canvas","canvas",800,800);
	c->Divide(2,2);
	//Load files
	TFile* f1 = new TFile("rot_z/trace_f1_0.01_refl@+0.5degz.root");
	TFile* f2 = new TFile("rot_z/trace_f2_0.01_refl@0.5degz.root");
	TFile* f3 = new TFile("rot_z/trace_f3_0.01_refl@+0.5degz.root");
	TFile* start_f1f2f3 = new TFile("pre_shoot/f1f2f3_div0.1_+0.5degz.root");
	TFile* notilt_f1f2f3 = new TFile("pre_shoot/f1f2f3_div0.1_notilt.root");
	TH2F* h_init = (TH2F*)start_f1f2f3->FindObjectAny(Form("h%i",inpt));
	h_init->SetTitle("Filament light arriving at foil, reflector tilt +0.5 deg about z");
	TH2F* h_foil = (TH2F*)f1->FindObjectAny("h0");
	h_foil->SetTitle("Filament light 20mm after foil");
	TH2F* h_final = (TH2F*)f1->FindObjectAny("h4");
	h_final->SetTitle("Final image at M4f");
	TH2F* h_notilt = (TH2F*)notilt_f1f2f3->FindObjectAny(Form("h%i",inpt));
	h_notilt->SetTitle("Filament light arriving at foil, no reflector tilt");

	c->cd(2);
	h_final->Draw("COLZ");
	c->cd(3);
	h_init->Draw("COLZ");
   	float dx = 6.557;
   	float dy = 4.;
   	float scale = dy/dx;
   	float diam = 1.2;
   	TEllipse *region = new TEllipse(0.,0.,25.,25.*scale);
  	region->SetFillStyle(0);
   	region->SetLineColor(kRed);
   	region->SetLineWidth(3);
   	TEllipse* holes[12];
   	for(int i = 0; i<3; i++){
        	holes[i] = new TEllipse((i+1)*dy,0.,diam,diam*scale);
        	holes[i+3] = new TEllipse(-(i+1)*dy,0.,diam,diam*scale);
        	holes[i+6] = new TEllipse(0.,(i+1)*dy,diam,diam*scale);
        	holes[i+9] = new TEllipse(0.,-(i+1)*dy,diam,diam*scale);
   	}
   	for(int i = 0; i<12; i++){
        	holes[i]->SetFillStyle(0);
        	holes[i]->SetLineColor(kRed);
        	holes[i]->SetLineWidth(2);
        	holes[i]->Draw();
   	}
   	//region->SetLineColor(kRed);
   	region->Draw();
	c->cd(4);
	h_foil->Draw("COLZ");
	region->Draw();
   	for(int i = 0; i<12; i++){
        	holes[i]->Draw();
   	}
	c->cd(1);
	h_notilt->Draw("COLZ");
	region->Draw();
   	for(int i = 0; i<12; i++){
        	holes[i]->Draw();
   	}
}
