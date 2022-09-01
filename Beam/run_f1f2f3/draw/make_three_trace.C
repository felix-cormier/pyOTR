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
void refl_macro(){
	//COLZ scheme
	set_plot_style();
	TCanvas* c = new TCanvas("canvas","canvas",800,800);
	c->Divide(2,2);
	//Load files
	TFile* f = new TFile("f1f2f3.root");
	TH2F* h1 = (TH2F*)f->FindObjectAny(Form("h1"));
	h1->SetTitle("F1 - Global Coordinates");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("x (mm)");
	TH2F* h2 = (TH2F*)f->FindObjectAny(Form("h2"));
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("x (mm)");
	h2->SetTitle("F2 - Global Coordinates");
	TH2F* h3 = (TH2F*)f->FindObjectAny(Form("h3"));
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("x (mm)");
	h3->SetTitle("F3 - Global Coordinates");

	c->cd(3);
	h1->Draw("COLZ");
	c->cd(4);
	h2->Draw("COLZ");
	c->cd(2);
	h3->Draw("COLZ");

}

void draw_foil(){
	set_plot_style();
	TCanvas* c = new TCanvas("canvas","canvas",800,800);
	c->Divide(2,2);
	//Load files
	TFile* f = new TFile("f1f2f3.root");
	TH2F* h1 = (TH2F*)f->FindObjectAny(Form("h1"));
	h1->SetTitle("F1 - Image Plane at Foil");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("x (mm)");
	TH2F* h2 = (TH2F*)f->FindObjectAny(Form("h2"));
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("x (mm)");
	h2->SetTitle("F2 - Image Plane at Foil");
	TH2F* h3 = (TH2F*)f->FindObjectAny(Form("h3"));
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("x (mm)");
	h3->SetTitle("F3 - Image Plane at Foil");
   	
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
	
	c->cd(2);
	h1->Draw("COLZ");
	region->Draw();
   	for(int i = 0; i<12; i++){
        	holes[i]->Draw();
   	}
	c->cd(4);
	h2->Draw("COLZ");
	region->Draw();
   	for(int i = 0; i<12; i++){
        	holes[i]->Draw();
   	}
	c->cd(3);
	h3->Draw("COLZ");
	region->Draw();
   	for(int i = 0; i<12; i++){
        	holes[i]->Draw();
   	}
}
