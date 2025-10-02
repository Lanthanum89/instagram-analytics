import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import requests
from io import BytesIO

from config import Config
from instagram_api import InstagramAPI
from data_analyzer import InstagramDataAnalyzer
from demo_data import DemoDataGenerator

class InstagramAnalyticsGUI:
    """Main GUI application for Instagram Analytics"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.configure(bg='white')
        
        # Initialize components
        self.api = None
        self.analyzer = InstagramDataAnalyzer()
        self.demo_generator = DemoDataGenerator()
        
        # Data storage
        self.current_data = {
            'account_info': {},
            'media_data': [],
            'insights_data': {},
            'posting_patterns': {}
        }
        
        # Create GUI components
        self.create_widgets()
        self.setup_styles()
        
        # Check configuration on startup
        self.check_configuration()
    
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground=Config.THEME_COLOR)
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Instagram Analytics Dashboard", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Right panel - Data display
        self.create_data_panel(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configuration section
        config_frame = ttk.LabelFrame(control_frame, text="Configuration", padding="5")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(config_frame, text="Setup API Credentials", 
                  command=self.setup_credentials, style='Custom.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(config_frame, text="Test Connection", 
                  command=self.test_connection, style='Custom.TButton').pack(fill=tk.X, pady=2)
        
        # Data fetching section
        data_frame = ttk.LabelFrame(control_frame, text="Data Collection", padding="5")
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(data_frame, text="Fetch Account Data", 
                  command=self.fetch_account_data, style='Custom.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="Fetch Recent Posts", 
                  command=self.fetch_recent_posts, style='Custom.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="Fetch Insights", 
                  command=self.fetch_insights, style='Custom.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="Analyze All Data", 
                  command=self.analyze_all_data, style='Custom.TButton').pack(fill=tk.X, pady=2)
        
        # Demo section
        demo_frame = ttk.LabelFrame(control_frame, text="Demo Mode", padding="5")
        demo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(demo_frame, text="Load Demo Data", 
                  command=self.load_demo_data, style='Custom.TButton').pack(fill=tk.X, pady=2)
        
        # Export section
        export_frame = ttk.LabelFrame(control_frame, text="Export", padding="5")
        export_frame.pack(fill=tk.X)
        
        ttk.Button(export_frame, text="Export Report", 
                  command=self.export_report, style='Custom.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="Save Charts", 
                  command=self.save_charts, style='Custom.TButton').pack(fill=tk.X, pady=2)
    
    def create_data_panel(self, parent):
        """Create the data display panel"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Account Overview tab
        self.create_overview_tab()
        
        # Posts Analysis tab
        self.create_posts_tab()
        
        # Charts tab
        self.create_charts_tab()
        
        # Insights tab
        self.create_insights_tab()
    
    def create_overview_tab(self):
        """Create account overview tab"""
        overview_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(overview_frame, text="Account Overview")
        
        # Account info display
        self.account_info_text = tk.Text(overview_frame, height=15, width=50, 
                                        font=('Arial', 10), state=tk.DISABLED)
        self.account_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for text widget
        scrollbar = ttk.Scrollbar(overview_frame, orient=tk.VERTICAL, 
                                 command=self.account_info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.account_info_text.configure(yscrollcommand=scrollbar.set)
    
    def create_posts_tab(self):
        """Create posts analysis tab"""
        posts_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(posts_frame, text="Posts Analysis")
        
        # Posts listbox with scrollbar
        posts_list_frame = ttk.Frame(posts_frame)
        posts_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.posts_listbox = tk.Listbox(posts_list_frame, font=('Arial', 9))
        posts_scrollbar = ttk.Scrollbar(posts_list_frame, orient=tk.VERTICAL,
                                       command=self.posts_listbox.yview)
        
        self.posts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        posts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.posts_listbox.configure(yscrollcommand=posts_scrollbar.set)
    
    def create_charts_tab(self):
        """Create charts tab"""
        charts_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(charts_frame, text="Charts")
        
        # Chart display area
        self.chart_frame = ttk.Frame(charts_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chart controls
        chart_controls = ttk.Frame(charts_frame)
        chart_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(chart_controls, text="Engagement Chart", 
                  command=self.show_engagement_chart).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(chart_controls, text="Posting Pattern", 
                  command=self.show_posting_pattern_chart).pack(side=tk.LEFT)
    
    def create_insights_tab(self):
        """Create insights tab"""
        insights_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(insights_frame, text="Insights")
        
        # Insights display
        self.insights_text = tk.Text(insights_frame, height=20, width=60, 
                                    font=('Arial', 10), state=tk.DISABLED)
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for insights
        insights_scrollbar = ttk.Scrollbar(insights_frame, orient=tk.VERTICAL,
                                          command=self.insights_text.yview)
        insights_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.insights_text.configure(yscrollcommand=insights_scrollbar.set)
    
    def check_configuration(self):
        """Check if API credentials are configured"""
        missing_fields = Config.validate_config()
        if missing_fields:
            self.status_var.set(f"Configuration incomplete: {', '.join(missing_fields)}")
            messagebox.showwarning("Configuration Required", 
                                 f"Please configure the following fields:\n{', '.join(missing_fields)}\n\nClick 'Setup API Credentials' to configure.")
        else:
            self.status_var.set("Configuration complete")
    
    def setup_credentials(self):
        """Open credentials setup dialog"""
        self.show_credentials_dialog()
    
    def show_credentials_dialog(self):
        """Show credentials configuration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("API Credentials Setup")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Instructions
        instructions = tk.Text(dialog, height=8, wrap=tk.WORD, font=('Arial', 9))
        instructions.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = """To use this app with real Instagram data, you need:

1. Meta for Developers account (developers.facebook.com)
2. Create a new app in Meta for Developers
3. Add Instagram Basic Display product to your app
4. Generate an access token with instagram_basic scope
5. Get your Instagram Business Account ID

For demo purposes, you can use the 'Load Demo Data' button instead."""
        
        instructions.insert(tk.END, instructions_text)
        instructions.configure(state=tk.DISABLED)
        
        # Credentials form
        form_frame = ttk.LabelFrame(dialog, text="Credentials", padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create entry fields
        fields = [
            ('Access Token:', 'META_ACCESS_TOKEN'),
            ('App ID:', 'META_APP_ID'),
            ('App Secret:', 'META_APP_SECRET'),
            ('Instagram Account ID:', 'INSTAGRAM_ACCOUNT_ID')
        ]
        
        entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(form_frame, width=50, show='*' if 'secret' in label.lower() else None)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
            entries[field] = entry
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Save", 
                  command=lambda: self.save_credentials(entries, dialog)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side=tk.RIGHT)
    
    def save_credentials(self, entries, dialog):
        """Save credentials (in real app, would save to .env file)"""
        # In a real application, you would save these to a .env file
        # For demo purposes, we'll just show a message
        messagebox.showinfo("Credentials", 
                           "In a real application, credentials would be saved to a .env file.\n\nFor now, use 'Load Demo Data' to see the app functionality.")
        dialog.destroy()
    
    def test_connection(self):
        """Test API connection"""
        try:
            self.api = InstagramAPI()
            if self.api.validate_token():
                messagebox.showinfo("Connection Test", "Successfully connected to Instagram API!")
                self.status_var.set("API connection successful")
            else:
                messagebox.showerror("Connection Test", "Failed to connect to Instagram API. Please check your credentials.")
                self.status_var.set("API connection failed")
        except Exception as e:
            messagebox.showerror("Connection Test", f"Error testing connection: {str(e)}")
            self.status_var.set("Connection test error")
    
    def fetch_account_data(self):
        """Fetch account data in a separate thread"""
        if not self.api:
            messagebox.showwarning("API Not Connected", "Please test connection first or use demo data.")
            return
        
        def fetch_data():
            self.status_var.set("Fetching account data...")
            try:
                account_info = self.api.get_account_info()
                if account_info:
                    self.current_data['account_info'] = self.analyzer.process_account_data(account_info)
                    self.update_overview_display()
                    self.status_var.set("Account data fetched successfully")
                else:
                    self.status_var.set("Failed to fetch account data")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def fetch_recent_posts(self):
        """Fetch recent posts data"""
        if not self.api:
            messagebox.showwarning("API Not Connected", "Please test connection first or use demo data.")
            return
        
        def fetch_data():
            self.status_var.set("Fetching recent posts...")
            try:
                media_data = self.api.get_recent_media(limit=25)
                if media_data:
                    self.current_data['media_data'] = self.analyzer.process_media_data(media_data)
                    self.update_posts_display()
                    self.status_var.set("Posts data fetched successfully")
                else:
                    self.status_var.set("Failed to fetch posts data")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def fetch_insights(self):
        """Fetch insights data"""
        if not self.api:
            messagebox.showwarning("API Not Connected", "Please test connection first or use demo data.")
            return
        
        def fetch_data():
            self.status_var.set("Fetching insights...")
            try:
                insights_data = self.api.get_account_insights()
                if insights_data:
                    self.current_data['insights_data'] = self.analyzer.process_insights_data(insights_data)
                    self.update_insights_display()
                    self.status_var.set("Insights fetched successfully")
                else:
                    self.status_var.set("Failed to fetch insights")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def analyze_all_data(self):
        """Analyze all available data"""
        if not self.current_data['media_data']:
            messagebox.showwarning("No Data", "Please fetch posts data first or load demo data.")
            return
        
        self.status_var.set("Analyzing data...")
        
        # Analyze posting patterns
        self.current_data['posting_patterns'] = self.analyzer.analyze_posting_patterns(self.current_data['media_data'])
        
        # Update all displays
        self.update_overview_display()
        self.update_posts_display()
        self.update_insights_display()
        
        self.status_var.set("Data analysis complete")
        messagebox.showinfo("Analysis Complete", "Data analysis completed successfully!")
    
    def load_demo_data(self):
        """Load demo data for testing"""
        self.status_var.set("Loading demo data...")
        
        # Generate demo data
        demo_data = self.demo_generator.generate_complete_dataset()
        
        # Process demo data
        self.current_data['account_info'] = demo_data['account_info']
        self.current_data['media_data'] = demo_data['media_data']
        self.current_data['insights_data'] = demo_data['insights_data']
        self.current_data['posting_patterns'] = self.analyzer.analyze_posting_patterns(demo_data['media_data'])
        
        # Update displays
        self.update_overview_display()
        self.update_posts_display()
        self.update_insights_display()
        
        self.status_var.set("Demo data loaded successfully")
        messagebox.showinfo("Demo Data", "Demo data loaded successfully! Explore the different tabs to see the analytics.")
    
    def update_overview_display(self):
        """Update the account overview display"""
        self.account_info_text.configure(state=tk.NORMAL)
        self.account_info_text.delete(1.0, tk.END)
        
        if self.current_data['account_info']:
            account = self.current_data['account_info']
            media_data = self.current_data['media_data']
            
            # Calculate additional metrics
            engagement_rate = 0
            if media_data and account.get('followers_count', 0) > 0:
                engagement_rate = self.analyzer.calculate_engagement_rate(
                    media_data, account['followers_count']
                )
            
            overview_text = f"""
📊 ACCOUNT OVERVIEW
{'='*50}

👤 Profile Information:
   Username: @{account.get('username', 'N/A')}
   Display Name: {account.get('name', 'N/A')}
   Biography: {account.get('biography', 'N/A')}

📈 Statistics:
   Followers: {account.get('followers_count', 0):,}
   Following: {account.get('follows_count', 0):,}
   Posts: {account.get('media_count', 0):,}
   Engagement Rate: {engagement_rate}%

📅 Recent Activity:
   Total Recent Posts Analyzed: {len(media_data)}
   """
            
            if self.current_data['posting_patterns']:
                patterns = self.current_data['posting_patterns']
                overview_text += f"""

⏰ Posting Patterns:
   Best Posting Hour: {patterns.get('best_hour', 'N/A')}:00
   Best Day: {patterns.get('best_day', 'N/A')}
"""
            
            # Top performing posts
            if media_data:
                top_posts = self.analyzer.get_top_performing_posts(media_data, 3)
                overview_text += "\n\n🏆 Top Performing Posts:\n"
                for i, post in enumerate(top_posts, 1):
                    overview_text += f"   {i}. {post['caption'][:50]}... (Engagement: {post['engagement']})\n"
            
            self.account_info_text.insert(tk.END, overview_text)
        else:
            self.account_info_text.insert(tk.END, "No account data available. Please fetch data or load demo data.")
        
        self.account_info_text.configure(state=tk.DISABLED)
    
    def update_posts_display(self):
        """Update the posts analysis display"""
        self.posts_listbox.delete(0, tk.END)
        
        if self.current_data['media_data']:
            for i, post in enumerate(self.current_data['media_data']):
                post_info = f"{i+1}. {post['media_type']} | Likes: {post['like_count']} | Comments: {post['comments_count']} | {post['caption']}"
                self.posts_listbox.insert(tk.END, post_info)
    
    def update_insights_display(self):
        """Update the insights display"""
        self.insights_text.configure(state=tk.NORMAL)
        self.insights_text.delete(1.0, tk.END)
        
        insights_content = "📊 INSTAGRAM INSIGHTS\n" + "="*50 + "\n\n"
        
        # Account insights
        if self.current_data['insights_data']:
            insights_content += "📈 Account Metrics:\n"
            for metric, value in self.current_data['insights_data'].items():
                insights_content += f"   {metric.replace('_', ' ').title()}: {value:,}\n"
            insights_content += "\n"
        
        # Posting patterns
        if self.current_data['posting_patterns']:
            patterns = self.current_data['posting_patterns']
            insights_content += "⏰ Posting Pattern Analysis:\n"
            insights_content += f"   Optimal Posting Hour: {patterns.get('best_hour', 'N/A')}:00\n"
            insights_content += f"   Best Day to Post: {patterns.get('best_day', 'N/A')}\n\n"
            
            if patterns.get('day_distribution'):
                insights_content += "   Posts by Day of Week:\n"
                for day, count in patterns['day_distribution'].items():
                    insights_content += f"     {day}: {count} posts\n"
        
        # Engagement analysis
        if self.current_data['media_data']:
            media_data = self.current_data['media_data']
            total_engagement = sum(post['engagement'] for post in media_data)
            avg_engagement = total_engagement / len(media_data) if media_data else 0
            
            insights_content += f"\n💝 Engagement Analysis:\n"
            insights_content += f"   Total Posts Analyzed: {len(media_data)}\n"
            insights_content += f"   Total Engagement: {total_engagement:,}\n"
            insights_content += f"   Average Engagement per Post: {avg_engagement:.1f}\n"
            
            # Top posts
            top_posts = self.analyzer.get_top_performing_posts(media_data, 5)
            insights_content += f"\n   Top 5 Posts by Engagement:\n"
            for i, post in enumerate(top_posts, 1):
                insights_content += f"     {i}. {post['engagement']} engagements - {post['caption'][:60]}...\n"
        
        if not any(self.current_data.values()):
            insights_content = "No insights available. Please fetch data or load demo data first."
        
        self.insights_text.insert(tk.END, insights_content)
        self.insights_text.configure(state=tk.DISABLED)
    
    def show_engagement_chart(self):
        """Show engagement trend chart"""
        if not self.current_data['media_data']:
            messagebox.showwarning("No Data", "Please load data first.")
            return
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create engagement chart
        fig = self.analyzer.create_engagement_chart(self.current_data['media_data'])
        if fig:
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_posting_pattern_chart(self):
        """Show posting pattern chart"""
        if not self.current_data['posting_patterns']:
            messagebox.showwarning("No Data", "Please analyze data first.")
            return
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create posting pattern chart
        fig = self.analyzer.create_posting_pattern_chart(self.current_data['posting_patterns'])
        if fig:
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def export_report(self):
        """Export analysis report"""
        if not any(self.current_data.values()):
            messagebox.showwarning("No Data", "Please load data first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Analysis Report"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Instagram Analytics Report\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    # Account info
                    if self.current_data['account_info']:
                        account = self.current_data['account_info']
                        f.write(f"Account: @{account.get('username', 'N/A')}\n")
                        f.write(f"Followers: {account.get('followers_count', 0):,}\n")
                        f.write(f"Posts: {account.get('media_count', 0):,}\n\n")
                    
                    # Engagement metrics
                    if self.current_data['media_data']:
                        media_data = self.current_data['media_data']
                        total_engagement = sum(post['engagement'] for post in media_data)
                        avg_engagement = total_engagement / len(media_data) if media_data else 0
                        
                        f.write(f"Total Posts Analyzed: {len(media_data)}\n")
                        f.write(f"Average Engagement: {avg_engagement:.1f}\n\n")
                        
                        # Top posts
                        top_posts = self.analyzer.get_top_performing_posts(media_data, 10)
                        f.write("Top Performing Posts:\n")
                        for i, post in enumerate(top_posts, 1):
                            f.write(f"{i}. Engagement: {post['engagement']} - {post['caption'][:100]}...\n")
                
                messagebox.showinfo("Export Complete", f"Report saved to {filename}")
                self.status_var.set("Report exported successfully")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save report: {str(e)}")
    
    def save_charts(self):
        """Save charts as images"""
        if not self.current_data['media_data']:
            messagebox.showwarning("No Data", "Please load data first.")
            return
        
        directory = filedialog.askdirectory(title="Select Directory to Save Charts")
        if directory:
            try:
                # Save engagement chart
                engagement_fig = self.analyzer.create_engagement_chart(self.current_data['media_data'])
                if engagement_fig:
                    engagement_fig.savefig(f"{directory}/engagement_chart.png", dpi=300, bbox_inches='tight')
                
                # Save posting pattern chart
                if self.current_data['posting_patterns']:
                    pattern_fig = self.analyzer.create_posting_pattern_chart(self.current_data['posting_patterns'])
                    if pattern_fig:
                        pattern_fig.savefig(f"{directory}/posting_pattern_chart.png", dpi=300, bbox_inches='tight')
                
                messagebox.showinfo("Charts Saved", f"Charts saved to {directory}")
                self.status_var.set("Charts saved successfully")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save charts: {str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = InstagramAnalyticsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()