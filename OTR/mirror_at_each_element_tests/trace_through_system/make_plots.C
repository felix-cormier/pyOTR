void set_plot_style()
{
    const Int_t NRGBs = 5;
    const Int_t NCont = 255;
    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
}

void draw(){
	TFile* f1 = new TFile("rot_z/trace_f1_0.01_refl@+0.5degz.root");
	TFile* f2 = new TFile("rot_z/trace_f2_0.01_refl@0.5degz.root");
	TFile* f3 = new TFile("rot_z/trace_f3_0.01_refl@+0.5degz.root");
	TH2F* h1 = (TH2F*)f1->Get("h4");
	TH2F* h2 = (TH2F*)f2->Get("h4");
	TH2F* h3 = (TH2F*)f3->Get("h4");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("y (mm)");
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("y (mm)");
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("y (mm)");
	h1->SetMarkerColor(kRed);
	h2->SetMarkerColor(kBlue);
	h3->SetMarkerColor(kBlack);
	h1->Draw("scat");
	h2->Draw("SAME");
	h3->Draw("SAME");
}


void cmp_rot(){
	TCanvas* c = new TCanvas("canvas","canvas",800,400);
	c->Divide(2,1);
	
	TFile* f1 = new TFile("rot_z/trace_f1_0.01_refl@+0.5degz.root");
	TFile* f2 = new TFile("rot_x/trace_f2_0.01_refl@+0.5degx.root");
	TFile* f3 = new TFile("rot_x/trace_f3_0.01_refl@+0.5degx.root");
	TFile* f11 = new TFile("no_rot/trace_f1_par.root");
	TFile* f22 = new TFile("no_rot/trace_f2_par.root");
	TFile* f33 = new TFile("no_rot/trace_f3_par.root");
	TH2F* h1 = (TH2F*)f1->Get("h4");
	h1->SetTitle("F1 - Reflector rotated +0.5 about z");
	TH2F* h2 = (TH2F*)f2->Get("h4");
	h2->SetTitle("F2 - Reflector rotated +0.5 about z");
	TH2F* h3 = (TH2F*)f3->Get("h4");
	h3->SetTitle("F3 - Reflector rotated +0.5 about z");
	TH2F* h11 = (TH2F*)f11->Get("h4");
	h11->SetTitle("F1 - Reflector rotated +0.5 about z");
	TH2F* h22 = (TH2F*)f22->Get("h4");
	h22->SetTitle("F2 - Reflector rotated +0.5 about x");
	TH2F* h33 = (TH2F*)f33->Get("h4");
	h33->SetTitle("F3 - Reflector rotated +0.5 about x");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("y (mm)");
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("y (mm)");
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("y (mm)");
	h1->SetMarkerColor(kRed);
	h2->SetMarkerColor(kRed);
	h3->SetMarkerColor(kRed);
	h11->SetMarkerColor(kBlack);
	h22->SetMarkerColor(kBlack);
	h33->SetMarkerColor(kBlack);
	c->cd(1);
	h22->Draw("scat");
	h2->Draw("SAME");
	c->cd(2);
	h33->Draw("scat");
	h3->Draw("SAME");
	//c->cd(4);
	//h33->Draw("scat");
	//h3->Draw("SAME");

}
