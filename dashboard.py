import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="RM Intelligence Dashboard",
    layout="wide",  # Uses full width of screen
    initial_sidebar_state="collapsed"  # Hide sidebar for cleaner look
)

# Custom CSS for professional banking look
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79, #4a90e2);
    padding: 1rem 2rem;
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 2rem;
    text-align: center;
}

.client-summary {
    background: #f8fbff;
    border: 1px solid #e6f3ff;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.evidence-item {
    background: #fafafa;
    border-left: 4px solid #4a90e2;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 4px 4px 0;
}

.kg-insight {
    background: #e8f5e8;
    border-left: 4px solid #4CAF50;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 4px 4px 0;
}

.metric-container {
    text-align: center;
    padding: 1rem;
    background: linear-gradient(135deg, #f8fbff, #e6f3ff);
    border-radius: 8px;
    border-left: 4px solid #4a90e2;
}
</style>
""", unsafe_allow_html=True)

# Sample client data - In real app, this would come from your database
CLIENT_DATA = {
    "Sarah Johnson": {
        "income": 85000,
        "monthly_expenses": 4200,
        "savings": 45000,
        "credit_score": 750,
        "employment": "Tech Company (3 yrs)",
        "age": 32,
        "debt": 15000
    },
    "Michael Chen": {
        "income": 92000,
        "monthly_expenses": 3800,
        "savings": 65000,
        "credit_score": 780,
        "employment": "Finance Firm (5 yrs)",
        "age": 29,
        "debt": 8000
    },
    "Emma Williams": {
        "income": 78000,
        "monthly_expenses": 4500,
        "savings": 32000,
        "credit_score": 720,
        "employment": "Healthcare (2 yrs)",
        "age": 35,
        "debt": 22000
    }
}

# Function to analyze query and determine metrics
def analyze_query(query_text):
    """
    Simple function to determine what type of analysis based on query keywords
    In real app, this would be replaced by your LLM processing
    """
    query_lower = query_text.lower()
    
    if any(word in query_lower for word in ['loan', 'borrow', 'credit']):
        return "loan_analysis"
    elif any(word in query_lower for word in ['investment', 'invest', 'portfolio']):
        return "investment_analysis"
    elif any(word in query_lower for word in ['mortgage', 'home', 'house']):
        return "mortgage_analysis"
    elif any(word in query_lower for word in ['card', 'credit card']):
        return "card_analysis"
    else:
        return "general_analysis"

# Function to get dynamic metrics based on analysis type
def get_metrics_and_analysis(client_data, analysis_type, query):
    """
    Returns appropriate metrics and analysis based on query type
    In real app, this would call your RAG pipeline
    """
    if analysis_type == "loan_analysis":
        # Calculate loan-specific metrics
        max_loan = min(client_data["income"] * 0.4, 50000)  # 40% of annual income, max 50k
        risk_score = 10 - (client_data["credit_score"] - 600) / 20  # Simple risk calculation
        
        return {
            "metric1_label": "Risk Score",
            "metric1_value": f"{risk_score:.1f}",
            "metric2_label": "Max Recommended",
            "metric2_value": f"${max_loan:,.0f}",
            "analysis_title": "Personal Loan Assessment",
            "analysis_text": f"""
            Based on {st.session_state.selected_client}'s financial profile, they qualify for a personal loan with {'low' if risk_score < 5 else 'moderate'} risk. 
            Their stable income of ${client_data['income']:,}, credit score of {client_data['credit_score']}, and savings of ${client_data['savings']:,} 
            indicate strong repayment capability.
            
            **Recommendation:** Approve personal loan up to ${max_loan:,.0f} at standard interest rate. 
            Their debt-to-income ratio would remain within acceptable limits.
            
            **Risk Factors:** Monitor employment stability and ensure loan terms include flexible payment options.
            """
        }
    
    elif analysis_type == "investment_analysis":
        savings_rate = (client_data["savings"] / client_data["income"]) * 100
        risk_tolerance = "Moderate" if client_data["age"] < 40 else "Conservative"
        
        return {
            "metric1_label": "Savings Rate",
            "metric1_value": f"{savings_rate:.1f}%",
            "metric2_label": "Risk Profile",
            "metric2_value": risk_tolerance,
            "analysis_title": "Investment Recommendation",
            "analysis_text": f"""
            {st.session_state.selected_client} shows excellent savings discipline with a {savings_rate:.1f}% savings rate. 
            Based on their age ({client_data['age']}) and financial stability, a {risk_tolerance.lower()} investment approach is recommended.
            
            **Recommendation:** Diversified portfolio with 60% equity, 30% bonds, 10% alternatives. 
            Consider increasing monthly investment contributions.
            
            **Next Steps:** Schedule portfolio review and discuss long-term financial goals.
            """
        }
    
    else:  # Default general analysis
        debt_to_income = (client_data["debt"] / client_data["income"]) * 100
        financial_health = "Excellent" if debt_to_income < 20 else "Good" if debt_to_income < 30 else "Fair"
        
        return {
            "metric1_label": "Debt-to-Income",
            "metric1_value": f"{debt_to_income:.1f}%",
            "metric2_label": "Financial Health",
            "metric2_value": financial_health,
            "analysis_title": "Financial Overview",
            "analysis_text": f"""
            {st.session_state.selected_client}'s overall financial health is {financial_health.lower()}. 
            With a debt-to-income ratio of {debt_to_income:.1f}% and strong credit score of {client_data['credit_score']}, 
            they are well-positioned for various financial products.
            
            **Strengths:** Stable employment, good credit history, healthy savings balance.
            
            **Opportunities:** Consider debt consolidation and investment portfolio optimization.
            """
        }

# Function to generate mock evidence
def get_evidence_data(client_name, analysis_type):
    """
    Mock function to generate evidence data
    In real app, this would query your knowledge graph and vector database
    """
    kg_insights = [
        f"Employment stability: {client_name} shows consistent employment history with good sector performance",
        f"Financial behavior: Regular savings patterns indicate disciplined money management",
        f"Credit relationships: Strong payment history with existing financial institutions"
    ]
    
    vector_docs = [
        {"source": "Client Email - Dec 2024", "text": "Looking for financial advice on loan consolidation and investment options..."},
        {"source": "Pay Stub Analysis - Nov 2024", "text": "Consistent monthly income with regular bonuses indicating stable employment"},
        {"source": "Bank Statement - Oct 2024", "text": "Regular savings deposits and controlled spending patterns show financial discipline"},
        {"source": "Industry Report - Nov 2024", "text": f"{client_name}'s employment sector showing stable growth despite market conditions"}
    ]
    
    return kg_insights, vector_docs

# Initialize session state for storing selected client
if 'selected_client' not in st.session_state:
    st.session_state.selected_client = "Sarah Johnson"

# Main header
st.markdown('<div class="main-header">🏦 RM Intelligence Dashboard</div>', unsafe_allow_html=True)

# Create three columns with specific widths
col1, col2, col3 = st.columns([1, 2, 1.2])

# COLUMN 1: Query Section
with col1:
    st.subheader("Query")
    
    # Client selection dropdown
    selected_client = st.selectbox(
        "Select Client",
        options=list(CLIENT_DATA.keys()),
        key="client_selector"
    )
    
    # Update session state when client changes
    if selected_client != st.session_state.selected_client:
        st.session_state.selected_client = selected_client
    
    # Get client data for selected client
    client_data = CLIENT_DATA[st.session_state.selected_client]
    
    # Client summary section
    st.markdown("**Quick Summary**")
    st.markdown(f"""
    <div class="client-summary">
        <div class="summary-row"><span>Annual Income:</span> <strong>${client_data['income']:,}</strong></div>
        <div class="summary-row"><span>Monthly Expenses:</span> <strong>${client_data['monthly_expenses']:,}</strong></div>
        <div class="summary-row"><span>Savings:</span> <strong>${client_data['savings']:,}</strong></div>
        <div class="summary-row"><span>Credit Score:</span> <strong>{client_data['credit_score']}</strong></div>
        <div class="summary-row"><span>Employment:</span> <strong>{client_data['employment']}</strong></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom query input
    custom_query = st.text_area(
        "Custom Query",
        value="What is the risk assessment for a personal loan of $50,000?",
        height=100,
        help="Enter your specific question about the client"
    )
    
    # Analyze button
    analyze_clicked = st.button("🔍 Analyze Client", type="primary", use_container_width=True)

# COLUMN 2: Analysis Results
with col2:
    st.subheader("Analysis Results")
    
    if analyze_clicked or custom_query:
        # Analyze the query type
        analysis_type = analyze_query(custom_query)
        
        # Get metrics and analysis
        results = get_metrics_and_analysis(client_data, analysis_type, custom_query)
        
        # Display metrics in two columns
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                label=results["metric1_label"],
                value=results["metric1_value"],
                help=f"Based on {st.session_state.selected_client}'s financial profile"
            )
        
        with metric_col2:
            st.metric(
                label=results["metric2_label"],
                value=results["metric2_value"],
                help="Calculated using our risk assessment model"
            )
        
        # Analysis content
        st.markdown(f"### {results['analysis_title']}")
        st.markdown(results["analysis_text"])
        
    else:
        # Placeholder content when no analysis is performed
        st.info("👆 Select a client and click 'Analyze Client' to see results")
        
        # Show sample metrics as placeholder
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Risk Score", "---", help="Will show after analysis")
        with metric_col2:
            st.metric("Recommendation", "---", help="Will show after analysis")

# COLUMN 3: Evidence & Reasoning
with col3:
    st.subheader("Evidence & Reasoning")
    
    if analyze_clicked or custom_query:
        # Get evidence data
        kg_insights, vector_docs = get_evidence_data(st.session_state.selected_client, 
                                                   analyze_query(custom_query) if custom_query else "general")
        
        # Knowledge Graph Reasoning section
        with st.expander("🕸️ Knowledge Graph Reasoning", expanded=True):
            for insight in kg_insights:
                st.markdown(f"""
                <div class="kg-insight">
                    <small>{insight}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Vector DB Supporting Documents section
        with st.expander("📄 Vector DB Supporting Documents", expanded=True):
            for doc in vector_docs:
                st.markdown(f"""
                <div class="evidence-item">
                    <strong style="color: #1f4e79; font-size: 0.85em;">{doc['source']}</strong><br>
                    <small>{doc['text']}</small>
                </div>
                """, unsafe_allow_html=True)
                
    else:
        # Placeholder content
        st.info("Evidence and reasoning will appear here after analysis")
        
        with st.expander("🕸️ Knowledge Graph Reasoning"):
            st.write("Knowledge graph insights will be displayed here...")
            
        with st.expander("📄 Vector DB Supporting Documents"):
            st.write("Supporting documents will be shown here...")

# Footer
st.markdown("---")
st.markdown("*Dashboard powered by RAG Pipeline with Knowledge Graph and Vector Search*")